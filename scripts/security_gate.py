#!/usr/bin/env python3
"""CI gate: reject critical Trivy image vulnerabilities absent from a reviewed baseline."""
import argparse
import json
import sys
from pathlib import Path


def read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"No se pudo leer JSON de {path}: {exc}") from exc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", required=True)
    parser.add_argument("--baseline", required=True)
    args = parser.parse_args()
    try:
        report = read_json(args.report)
        baseline = read_json(args.baseline)
        if not isinstance(report, dict) or not isinstance(report.get("Results"), list):
            raise ValueError("El reporte Trivy debe contener una lista Results")
        if not isinstance(baseline, dict) or not isinstance(baseline.get("approved_critical"), list):
            raise ValueError("La línea base debe contener approved_critical como lista")
        approved = set()
        for item in baseline["approved_critical"]:
            if not isinstance(item, dict) or not all(isinstance(item.get(k), str) and item[k] for k in ("target", "vulnerability_id", "package")):
                raise ValueError("Entrada inválida en approved_critical")
            approved.add((item["target"], item["vulnerability_id"], item["package"]))
        detected = set()
        for result in report["Results"]:
            if not isinstance(result, dict):
                raise ValueError("Results contiene un elemento inválido")
            target = result.get("Target")
            vulnerabilities = result.get("Vulnerabilities", [])
            if not isinstance(target, str) or not isinstance(vulnerabilities, list):
                raise ValueError("Target o Vulnerabilities inválido en reporte")
            for vulnerability in vulnerabilities:
                if not isinstance(vulnerability, dict) or not isinstance(vulnerability.get("Severity"), str):
                    raise ValueError("Vulnerabilidad inválida en reporte")
                if vulnerability["Severity"].upper() == "CRITICAL":
                    vuln_id = vulnerability.get("VulnerabilityID")
                    package = vulnerability.get("PkgName")
                    if not isinstance(vuln_id, str) or not vuln_id or not isinstance(package, str) or not package:
                        raise ValueError("Vulnerabilidad crítica sin VulnerabilityID o PkgName")
                    detected.add((target, vuln_id, package))
        new = detected - approved
        print(f"Críticas detectadas: {len(detected)} | aprobadas en línea base: {len(detected & approved)} | nuevas: {len(new)}")
        for target, vid, package in sorted(new):
            print(f"BLOQUEO: {vid} | paquete={package} | objetivo={target}")
        if new:
            print("SECURITY GATE: BLOCKED")
            return 1
        print("SECURITY GATE: PASSED")
        return 0
    except ValueError as exc:
        print(f"SECURITY GATE: ERROR - {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
