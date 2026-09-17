import os
import re
import math

def run_tests():
    print("=== STARTING EMPIRICAL CHALLENGER VERIFICATION ===")
    errors = []

    # 1. Parse ground truth
    gt_file = r"d:\sandbox\work-box\dissertation-skills\research_sources\existing_work\Antibacterial Efficacy Results - Zone of Inhibition.md"
    with open(gt_file, "r", encoding="utf-8") as f:
        gt_text = f.read()

    expected_data = {
        "Ecoli": {
            "C1": {"R": [12.00, 11.78, 12.05], "mean": 11.94, "sd": 0.14},
            "C2": {"R": [15.00, 15.50, 14.48], "mean": 14.99, "sd": 0.51},
            "GEN5": {"R": [17.00, 17.00, 17.00], "mean": 17.00, "sd": 0.00},
            "N": {"R": [0.00, 0.00, 0.00], "mean": 0.00, "sd": 0.00}
        },
        "Paer": {
            "C1": {"R": [16.00, 16.30, 15.80], "mean": 16.03, "sd": 0.25},
            "C2": {"R": [13.00, 12.50, 12.10], "mean": 12.53, "sd": 0.45},
            "GEN5": {"R": [17.50, 17.00, 17.00], "mean": 17.17, "sd": 0.29},
            "N": {"R": [0.00, 0.00, 0.00], "mean": 0.00, "sd": 0.00}
        },
        "Kpneu": {
            "C1": {"R": [12.00, 13.00, 12.05], "mean": 12.35, "sd": 0.56},
            "C2": {"R": [13.50, 13.50, 12.75], "mean": 13.25, "sd": 0.43},
            "GEN5": {"R": [15.50, 15.00, 15.00], "mean": 15.17, "sd": 0.29},
            "N": {"R": [0.00, 0.00, 0.00], "mean": 0.00, "sd": 0.00}
        }
    }

    # Verify mathematical integrity of ground truth replicates
    print("\n--- 1. Checking mathematical integrity of ground truth replicates ---")
    for strain, treatments in expected_data.items():
        for trt, vals in treatments.items():
            r = vals["R"]
            calc_mean = sum(r) / len(r)
            if len(r) > 1:
                calc_sd = math.sqrt(sum((x - calc_mean) ** 2 for x in r) / (len(r) - 1))
            else:
                calc_sd = 0.0
            diff_mean = abs(calc_mean - vals["mean"])
            diff_sd = abs(calc_sd - vals["sd"])
            print(f"[{strain} - {trt}] R={r} -> calc: {calc_mean:.4f} +- {calc_sd:.4f} | truth: {vals['mean']} +- {vals['sd']}")
            if diff_mean > 0.005:
                errors.append(f"Ground truth mean mismatch for {strain} {trt}: calc {calc_mean:.4f} vs {vals['mean']}")
            if diff_sd > 0.005:
                errors.append(f"Ground truth SD mismatch for {strain} {trt}: calc {calc_sd:.4f} vs {vals['sd']}")

    # 2. Check chapters/04_results.tex Table 4.2
    print("\n--- 2. Checking chapters/04_results.tex Table 4.2 (tab:zoi) ---")
    res_path = r"d:\sandbox\work-box\dissertation-skills\chapters\04_results.tex"
    with open(res_path, "r", encoding="utf-8") as f:
        res_text = f.read()

    # Find Table 4.2 rows
    # \textit{E.\ coli} & 0.00 \pm 0.00 & 11.94 \pm 0.14 & 14.99 \pm 0.51 & 17.00 \pm 0.00 \\
    table_pattern = re.compile(r"\\textit\{([A-Za-z\.\\\s]+)\}\s*&\s*([0-9\.]+)\s*\\pm\s*([0-9\.]+)\s*&\s*([0-9\.]+)\s*\\pm\s*([0-9\.]+)\s*&\s*([0-9\.]+)\s*\\pm\s*([0-9\.]+)\s*&\s*([0-9\.]+)\s*\\pm\s*([0-9\.]+)")
    matches = table_pattern.findall(res_text)
    print(f"Found {len(matches)} rows in Table 4.2:")
    for m in matches:
        raw_s = m[0].replace(" ", "").replace("\\", "").replace(".", "")
        if "Ecoli" in raw_s:
            s_key = "Ecoli"
        elif "Paeruginosa" in raw_s:
            s_key = "Paer"
        elif "Kpneumoniae" in raw_s:
            s_key = "Kpneu"
        else:
            errors.append(f"Unrecognized strain in Table 4.2: {m[0]}")
            continue

        n_m, n_sd = float(m[1]), float(m[2])
        c1_m, c1_sd = float(m[3]), float(m[4])
        c2_m, c2_sd = float(m[5]), float(m[6])
        g_m, g_sd = float(m[7]), float(m[8])
        print(f"Row {s_key}: N={n_m}+-{n_sd}, C1={c1_m}+-{c1_sd}, C2={c2_m}+-{c2_sd}, GEN5={g_m}+-{g_sd}")
        
        # compare with expected
        if (n_m, n_sd) != (expected_data[s_key]["N"]["mean"], expected_data[s_key]["N"]["sd"]):
            errors.append(f"Table 4.2 N mismatch for {s_key}")
        if (c1_m, c1_sd) != (expected_data[s_key]["C1"]["mean"], expected_data[s_key]["C1"]["sd"]):
            errors.append(f"Table 4.2 C1 mismatch for {s_key}")
        if (c2_m, c2_sd) != (expected_data[s_key]["C2"]["mean"], expected_data[s_key]["C2"]["sd"]):
            errors.append(f"Table 4.2 C2 mismatch for {s_key}")
        if (g_m, g_sd) != (expected_data[s_key]["GEN5"]["mean"], expected_data[s_key]["GEN5"]["sd"]):
            errors.append(f"Table 4.2 GEN5 mismatch for {s_key}")

    # 3. Check TikZ coordinates in chapters/04_results.tex
    print("\n--- 3. Checking TikZ coordinates in chapters/04_results.tex (fig:zoibars) ---")
    tikz_c1 = re.search(r"\\addplot\+\[fill=dissertationblue!70[^\]]*\]\s*coordinates\s*\{([^}]+)\};", res_text)
    tikz_c2 = re.search(r"\\addplot\+\[fill=dissertationgreen!70[^\]]*\]\s*coordinates\s*\{([^}]+)\};", res_text)
    tikz_gen5 = re.search(r"\\addplot\+\[fill=dissertationgray!50[^\]]*\]\s*coordinates\s*\{([^}]+)\};", res_text)

    def parse_coords(coord_str):
        p = re.compile(r"\(([A-Za-z]+),([0-9\.]+)\)\s*\+-\(([0-9\.]+),([0-9\.]+)\)")
        return {m[0]: (float(m[1]), float(m[2]), float(m[3])) for m in p.findall(coord_str)}

    if tikz_c1:
        c1_coords = parse_coords(tikz_c1.group(1))
        print("TikZ C1 coords:", c1_coords)
        for s in ["Ecoli", "Paer", "Kpneu"]:
            val, s1, s2 = c1_coords[s]
            if val != expected_data[s]["C1"]["mean"] or s1 != expected_data[s]["C1"]["sd"] or s2 != expected_data[s]["C1"]["sd"]:
                errors.append(f"TikZ C1 mismatch for {s}: {c1_coords[s]}")
    else:
        errors.append("TikZ C1 plot not found in 04_results.tex")

    if tikz_c2:
        c2_coords = parse_coords(tikz_c2.group(1))
        print("TikZ C2 coords:", c2_coords)
        for s in ["Ecoli", "Paer", "Kpneu"]:
            val, s1, s2 = c2_coords[s]
            if val != expected_data[s]["C2"]["mean"] or s1 != expected_data[s]["C2"]["sd"] or s2 != expected_data[s]["C2"]["sd"]:
                errors.append(f"TikZ C2 mismatch for {s}: {c2_coords[s]}")
    else:
        errors.append("TikZ C2 plot not found in 04_results.tex")

    if tikz_gen5:
        gen5_coords = parse_coords(tikz_gen5.group(1))
        print("TikZ GEN 5 coords:", gen5_coords)
        for s in ["Ecoli", "Paer", "Kpneu"]:
            val, s1, s2 = gen5_coords[s]
            if val != expected_data[s]["GEN5"]["mean"] or s1 != expected_data[s]["GEN5"]["sd"] or s2 != expected_data[s]["GEN5"]["sd"]:
                errors.append(f"TikZ GEN5 mismatch for {s}: {gen5_coords[s]}")
    else:
        errors.append("TikZ GEN 5 plot not found in 04_results.tex")

    # 4. Check results prose numbers
    print("\n--- 4. Checking Results narrative text in 04_results.tex ---")
    prose_checks = [
        ("N control", r"Distilled water \(N\) gave \$0\.00 \\pm 0\.00\$\\,mm"),
        ("E. coli C1", r"Against \\taxa\{Escherichia coli\} the C1 mean was \$11\.94 \\pm 0\.14\$\\,mm"),
        ("E. coli C2", r"and the C2 mean was \$14\.99 \\pm 0\.51\$\\,mm"),
        ("E. coli GEN5", r"The GEN 5 disc measured \$17\.00 \\pm 0\.00\$\\,mm"),
        ("P. aer C1", r"Against \\taxa\{Pseudomonas aeruginosa\} the C1 mean was \$16\.03 \\pm 0\.25\$\\,mm"),
        ("P. aer C2", r"and the C2 mean was \$12\.53 \\pm 0\.45\$\\,mm"),
        ("P. aer GEN5", r"The GEN 5 disc measured \$17\.17 \\pm 0\.29\$\\,mm"),
        ("K. pneu C1", r"Against \\taxa\{Klebsiella pneumoniae\} the C1 mean was \$12\.35 \\pm 0\.56\$\\,mm"),
        ("K. pneu C2", r"and the C2 mean was \$13\.25 \\pm 0\.43\$\\,mm"),
        ("K. pneu GEN5", r"The GEN 5 disc measured \$15\.17 \\pm 0\.29\$\\,mm")
    ]
    for label, pat in prose_checks:
        if re.search(pat, res_text):
            print(f"[PASS] Found {label} exact text pattern")
        else:
            print(f"[FAIL] Missing {label} text pattern")
            errors.append(f"Results prose mismatch for {label}")

    # 5. Check appendices/appendix_a_zoi.tex Tables A.1 - A.3
    print("\n--- 5. Checking appendices/appendix_a_zoi.tex ---")
    app_path = r"d:\sandbox\work-box\dissertation-skills\appendices\appendix_a_zoi.tex"
    with open(app_path, "r", encoding="utf-8") as f:
        app_text = f.read()

    def parse_app_table(tbl_label):
        # split by \begin{table}
        tables = app_text.split(r"\begin{table}")
        for t in tables:
            if tbl_label in t:
                row_p = re.compile(r"([A-Z0-9\s]+)\s*&\s*([0-9\.]+)\s*&\s*([0-9\.]+)\s*&\s*([0-9\.]+)\s*\\\\")
                rows = {}
                for r in row_p.findall(t):
                    trt = r[0].strip().replace(" ", "")
                    rows[trt] = [float(r[1]), float(r[2]), float(r[3])]
                return rows
        return None

    app_tables = {
        "Ecoli": "tab:raw_ecoli",
        "Paer": "tab:raw_paer",
        "Kpneu": "tab:raw_kpneu"
    }
    for s_key, tbl_lbl in app_tables.items():
        rows = parse_app_table(tbl_lbl)
        print(f"Table {tbl_lbl} ({s_key}) parsed rows: {rows}")
        if not rows:
            errors.append(f"Table {tbl_lbl} not found in appendix_a_zoi.tex")
            continue
        for trt in ["C1", "C2", "GEN5", "N"]:
            exp_r = expected_data[s_key][trt]["R"]
            act_r = rows.get(trt)
            if act_r != exp_r:
                errors.append(f"Appendix table {tbl_lbl} mismatch for {trt}: got {act_r}, expected {exp_r}")

    # 6. Check Soxhlet yield 24.13% across Methods, Results, Discussion
    print("\n--- 6. Checking 24.13% yield across chapters ---")
    methods_path = r"d:\sandbox\work-box\dissertation-skills\chapters\03_methods.tex"
    disc_path = r"d:\sandbox\work-box\dissertation-skills\chapters\05_discussion.tex"

    with open(methods_path, "r", encoding="utf-8") as f:
        methods_text = f.read()
    with open(disc_path, "r", encoding="utf-8") as f:
        disc_text = f.read()

    if "24.13\\% (w/w)" in methods_text or "24.13%" in methods_text:
        print("[PASS] Methods mentions 24.13% yield")
    else:
        errors.append("Methods does not mention 24.13% yield")

    if "24.13\\% (w/w)" in res_text or "24.13%" in res_text:
        print("[PASS] Results mentions 24.13% yield")
    else:
        errors.append("Results does not mention 24.13% yield")

    if "24.13\\%" in disc_text or "24.13%" in disc_text:
        print("[PASS] Discussion mentions 24.13% yield")
    else:
        errors.append("Discussion does not mention 24.13% yield")

    # 7. Check GPS Coordinates
    print("\n--- 7. Checking GPS coordinates 34.12981 N, 74.83396 E ---")
    concl_path = r"d:\sandbox\work-box\dissertation-skills\chapters\06_conclusion.tex"
    with open(concl_path, "r", encoding="utf-8") as f:
        concl_text = f.read()

    coord_str_1 = "34.12981"
    coord_str_2 = "74.83396"
    for name, text in [("Methods", methods_text), ("Conclusion", concl_text)]:
        if coord_str_1 in text and coord_str_2 in text:
            print(f"[PASS] {name} contains coordinates 34.12981 N, 74.83396 E")
        else:
            errors.append(f"{name} missing coordinates")

    # 8. Check candidate metadata disclaimers
    print("\n--- 8. Checking honest candidate metadata disclaimers ---")
    disclaimers = {
        "voucher in methods": "herbarium voucher number was not available" in methods_text.lower(),
        "strain IDs in methods": "strain accession numbers (atcc or equivalent) were not supplied" in methods_text.lower(),
        "collection month / voucher in discussion": "collection month and a herbarium voucher number were not available" in disc_text.lower(),
        "well volume in discussion": "unrecorded extract well loading volume" in disc_text.lower()
    }
    for k, v in disclaimers.items():
        if v:
            print(f"[PASS] Disclaimer verified: {k}")
        else:
            print(f"[FAIL] Disclaimer missing: {k}")
            errors.append(f"Missing disclaimer: {k}")

    # 9. Check Table 5.1 in Discussion
    print("\n--- 9. Checking Table 5.1 in Discussion (tab:compare) ---")
    tab_compare_pat = re.compile(r"\\label\{tab:compare\}.*?\\end\{table\}", re.DOTALL)
    m_comp = tab_compare_pat.search(disc_text)
    if m_comp:
        comp_content = m_comp.group(0)
        print("[PASS] Table 5.1 found in Discussion")
        if "14.99 \\pm 0.51 & 12.53 \\pm 0.45" in comp_content:
            print("[PASS] C2 row in Table 5.1 matches exactly")
        else:
            errors.append("Table 5.1 C2 row mismatch")
        if "11.94 \\pm 0.14 & 16.03 \\pm 0.25" in comp_content:
            print("[PASS] C1 row in Table 5.1 matches exactly")
        else:
            errors.append("Table 5.1 C1 row mismatch")
        if "17.00 \\pm 0.00 & 17.17 \\pm 0.29" in comp_content:
            print("[PASS] GEN 5 row in Table 5.1 matches exactly")
        else:
            errors.append("Table 5.1 GEN 5 row mismatch")
    else:
        errors.append("Table 5.1 (tab:compare) not found in 05_discussion.tex")

    print("\n=== SUMMARY ===")
    if errors:
        print(f"FAILED with {len(errors)} errors:")
        for e in errors:
            print(f" - {e}")
        return False
    else:
        print("ALL EMPIRICAL TESTS PASSED WITH ZERO ERRORS!")
        return True

if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
