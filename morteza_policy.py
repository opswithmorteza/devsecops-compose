"""Audit normalized Docker Compose JSON. Standard library only; Python 3.11+."""
import json
import sys


def audit(config):
    findings = []
    services = config.get("services", {})
    if not services:
        return ["config: no services"]
    for name, service in services.items():
        def fail(message):
            findings.append(f"{name}: {message}")
        user = str(service.get("user", "")).split(":")[0]
        if not user.isdecimal() or int(user) == 0:
            fail("require explicit nonzero numeric UID")
        if service.get("privileged"):
            fail("privileged mode forbidden")
        if service.get("network_mode") == "host":
            fail("host networking forbidden")
        if service.get("pid") == "host":
            fail("host PID namespace forbidden")
        if not service.get("read_only"):
            fail("root filesystem must be read-only")
        if "ALL" not in service.get("cap_drop", []):
            fail("drop ALL capabilities")
        if service.get("cap_add"):
            fail("additional capabilities forbidden")
        opts = service.get("security_opt", [])
        if not any(str(opt) in ("no-new-privileges:true", "no-new-privileges=true") for opt in opts):
            fail("require no-new-privileges")
        health = service.get("healthcheck", {})
        if health.get("disable") or not health.get("test") or health["test"][0] == "NONE":
            fail("require active healthcheck")
        for port in service.get("ports", []):
            if not isinstance(port, dict) or port.get("host_ip") not in ("127.0.0.1", "::1"):
                fail("published ports must bind loopback")
        for volume in service.get("volumes", []):
            if isinstance(volume, dict) and volume.get("type") == "bind":
                fail("host bind mounts forbidden in this demo profile")
        if not service.get("mem_limit"):
            fail("require memory limit")
        if int(service.get("pids_limit", 0)) <= 0:
            fail("require positive PID limit")
    return findings


if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as source:
        findings = audit(json.load(source))
    print("\n".join(findings) if findings else "PASS: demo policy checks")
    sys.exit(bool(findings))
