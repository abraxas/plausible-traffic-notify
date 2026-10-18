#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-plausible-traffic-notify}"
export PYTHONUNBUFFERED=1
chmod +x poc.py

LABEL="plausible-traffic-notify"
WITNESS="PLAUSIBLE-H03-TRAFFIC-NOTIFY-SITEID-WITNESS"
PIN_SHA="d44e104ae3943a9240d5cb6b62e67dff0f069d3a"
PIN_IMAGE="plausible-lab:d44e104ae3943a"
PIN_REPO="https://github.com/plausible/analytics.git"

down() {
  echo "== docker compose down -v =="
  docker compose -p "${COMPOSE_PROJECT_NAME}" down -v --remove-orphans || true
}

fail_setup() {
  local reason="$1"
  echo "FAIL ${LABEL} ${reason} ${WITNESS}" | tee poc-last-run.txt
  docker compose -p "${COMPOSE_PROJECT_NAME}" logs --no-color --tail=120 plausible || true
  docker compose -p "${COMPOSE_PROJECT_NAME}" logs --no-color --tail=40 plausible_db || true
  docker compose -p "${COMPOSE_PROJECT_NAME}" logs --no-color --tail=40 plausible_events_db || true
  down
  exit 1
}

ensure_pin_image() {
  if docker image inspect "${PIN_IMAGE}" >/dev/null 2>&1; then
    echo "IOC image=${PIN_IMAGE} (prebuilt)"
    return 0
  fi
  echo "== clone pin ${PIN_SHA} =="
  rm -rf pin
  git clone --filter=blob:none --no-checkout "${PIN_REPO}" pin
  git -C pin fetch --depth 1 origin "${PIN_SHA}"
  git -C pin checkout --force "${PIN_SHA}"
  echo "== docker build ${PIN_IMAGE} MIX_ENV=ce =="
  docker build -t "${PIN_IMAGE}" --build-arg MIX_ENV=ce -f pin/Dockerfile pin
  echo "IOC image=${PIN_IMAGE} (built)"
}

trap down EXIT

echo "== docker compose down (clean) =="
down
ensure_pin_image
export PLAUSIBLE_IMAGE="${PIN_IMAGE}"

echo "== docker compose up =="
up_ok=0
for attempt in $(seq 1 8); do
  if PLAUSIBLE_IMAGE="${PLAUSIBLE_IMAGE}" docker compose -p "${COMPOSE_PROJECT_NAME}" up -d --no-build; then
    up_ok=1
    break
  fi
  echo "IOC compose-up-retry attempt=${attempt}"
  sleep 15
  down
done
if [[ "${up_ok}" != 1 ]]; then
  fail_setup "compose-up-failed"
fi

echo "== wait GET /api/health and /login =="
ready=0
for i in $(seq 1 90); do
  health="$(curl -sS -o /tmp/plausible-traffic-notify-health.txt -w '%{http_code}' --max-time 8 \
    "http://127.0.0.1:18183/api/health" || true)"
  login_code="$(curl -sS -o /tmp/plausible-traffic-notify-login.txt -w '%{http_code}' --max-time 8 \
    "http://127.0.0.1:18183/login" || true)"
  register_code="$(curl -sS -o /tmp/plausible-traffic-notify-register.txt -w '%{http_code}' --max-time 8 \
    "http://127.0.0.1:18183/register" || true)"
  echo "IOC wait attempt=${i} health=${health} login=${login_code} register=${register_code}"
  if [[ "${health}" == "200" ]] && { [[ "${login_code}" == "200" ]] || [[ "${login_code}" == "302" ]] || [[ "${register_code}" == "200" ]]; }; then
    ready=1
    break
  fi
  sleep 4
done
if [[ "${ready}" != 1 ]]; then
  fail_setup "plausible-not-ready"
fi

echo "== poc.py =="
set +e
python3 ./poc.py | tee poc-last-run.txt
rc=${PIPESTATUS[0]}
set -e

if ! tail -n1 poc-last-run.txt 2>/dev/null | grep -qE "^(SUCCESS|FAIL) ${LABEL} "; then
  echo "FAIL ${LABEL} poc-exit=${rc} ${WITNESS}" >> poc-last-run.txt
  rc=1
fi

exit "${rc}"
