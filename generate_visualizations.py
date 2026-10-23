"""Generate high-resolution visual graphics for Senior Management and Layman teams."""

import os
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

ARTIFACTS_DIR = r"C:\Users\bsank\.gemini\antigravity\brain\fda1237b-d0ff-46d9-abfb-f32a59a18689"
os.makedirs(ARTIFACTS_DIR, exist_ok=True)

# Set high-quality styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'


def plot_radar_comparison():
    """Figure 1: Radar (Spider) chart comparing the 3 candidates across 5 pillars."""
    categories = ['Target Potency\n(35%)', 'Kinome Selectivity\n(20%)', 'Liver & Patient Safety\n(25%)', 'Physical Balance (LipE)\n(10%)', 'Developability\n(10%)']
    N = len(categories)
    angles = [n / float(N) * 2 * math.pi for n in range(N)]
    angles += angles[:1]

    lead_scores = [1.0, 1.0, 1.0, 0.98, 1.0]
    lead_scores += lead_scores[:1]

    greasy_scores = [0.85, 0.25, 0.35, 0.20, 0.15]
    greasy_scores += greasy_scores[:1]

    tox_scores = [0.92, 0.95, 0.10, 0.88, 0.75]
    tox_scores += tox_scores[:1]

    fig, ax = plt.subplots(figsize=(8, 7), subplot_kw=dict(polar=True), dpi=200)
    plt.xticks(angles[:-1], categories, color='#1e293b', size=11, weight='bold')
    ax.set_rlabel_position(25)
    plt.yticks([0.25, 0.50, 0.75, 1.0], ["25%", "50%", "75%", "100% Target"], color="#64748b", size=9)
    plt.ylim(0, 1.1)

    # Lead Candidate
    ax.plot(angles, lead_scores, linewidth=2.5, linestyle='solid', color='#10b981', label='JAK2-LEAD-001 (Advance [GO])')
    ax.fill(angles, lead_scores, color='#10b981', alpha=0.25)

    # Greasy Trap
    ax.plot(angles, greasy_scores, linewidth=2.0, linestyle='dashed', color='#f59e0b', label='JAK2-GREASY-002 (Greasy Trap [STOP])')
    ax.fill(angles, greasy_scores, color='#f59e0b', alpha=0.15)

    # Tox Alert
    ax.plot(angles, tox_scores, linewidth=2.0, linestyle='dotted', color='#ef4444', label='JAK2-TOX-003 (Poison Pill [STOP])')
    ax.fill(angles, tox_scores, color='#ef4444', alpha=0.15)

    plt.title("Executive 5-Pillar Scorecard: The Balance of Power\nTarget: Full coverage in the outer ring", size=14, weight='bold', pad=25, color='#0f172a')
    plt.legend(loc='upper right', bbox_to_anchor=(1.25, 1.12), fontsize=10, frameon=True, facecolor='white', edgecolor='#e2e8f0')

    output_path = os.path.join(ARTIFACTS_DIR, "radar_scorecard_comparison.png")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_path}")


def plot_sweetspot_quadrant():
    """Figure 2: Potency vs Lipophilicity (cLogP) - The Sweet Spot Quadrant."""
    fig, ax = plt.subplots(figsize=(9, 6.5), dpi=200)

    # Zones
    ax.axvspan(1.5, 3.0, ymin=0.5, ymax=1.0, color='#10b981', alpha=0.12, label='Drug Hunter Sweet Spot (Target Zone)')
    ax.axvspan(3.0, 5.5, ymin=0.5, ymax=1.0, color='#f59e0b', alpha=0.08, label='Lipophilicity Trap Zone')
    ax.axvspan(1.5, 5.5, ymin=0.0, ymax=0.5, color='#64748b', alpha=0.05, label='Low Target Engagement Zone')

    # Threshold lines
    ax.axvline(3.0, color='#e11d48', linestyle='--', linewidth=1.5, label='TPP cLogP Limit (< 3.0)')
    ax.axhline(7.3, color='#2563eb', linestyle='--', linewidth=1.5, label='TPP Potency Limit (IC50 < 50 nM, pIC50 > 7.3)')

    # Diagonal LipE lines (LipE = pIC50 - cLogP -> pIC50 = LipE + cLogP)
    x_vals = np.linspace(1.5, 5.5, 100)
    ax.plot(x_vals, 5.0 + x_vals, color='#059669', linestyle=':', linewidth=1.2, alpha=0.7, label='LipE = 5.0 line')
    ax.plot(x_vals, 4.0 + x_vals, color='#d97706', linestyle=':', linewidth=1.2, alpha=0.7, label='LipE = 4.0 line')

    # Plot Candidates
    # LEAD-001: clogP=2.3, jak2_ic50=6.2 nM -> pIC50 = 8.21
    ax.scatter(2.3, 8.21, s=260, color='#10b981', edgecolor='#064e3b', linewidth=2.5, zorder=5)
    ax.annotate("JAK2-LEAD-001\n(cLogP: 2.3, IC50: 6.2 nM)\n[ADVANCE TO ANIMAL PK]",
                xy=(2.3, 8.21), xytext=(2.45, 8.45),
                arrowprops=dict(arrowstyle="->", color='#064e3b', lw=1.5),
                fontsize=9.5, weight='bold', color='#064e3b',
                bbox=dict(boxstyle="round,pad=0.4", fc="#d1fae5", ec="#10b981", lw=1.2))

    # GREASY-002: clogP=4.6, jak2_ic50=4.1 nM -> pIC50 = 8.39
    ax.scatter(4.6, 8.39, s=260, color='#f59e0b', edgecolor='#78350f', linewidth=2.5, zorder=5)
    ax.annotate("JAK2-GREASY-TRAP-002\n(cLogP: 4.6, IC50: 4.1 nM)\n[HIGH GREASE & INSOLUBLE]",
                xy=(4.6, 8.39), xytext=(3.4, 8.7),
                arrowprops=dict(arrowstyle="->", color='#78350f', lw=1.5),
                fontsize=9.5, weight='bold', color='#78350f',
                bbox=dict(boxstyle="round,pad=0.4", fc="#fef3c7", ec="#f59e0b", lw=1.2))

    # TOX-003: clogP=2.8, jak2_ic50=12.0 nM -> pIC50 = 7.92
    ax.scatter(2.8, 7.92, s=260, color='#ef4444', edgecolor='#7f1d1d', linewidth=2.5, zorder=5)
    ax.annotate("JAK2-TOX-ALERT-003\n(cLogP: 2.8, IC50: 12.0 nM)\n[FATAL REACTIVE METABOLITE]",
                xy=(2.8, 7.92), xytext=(3.0, 7.4),
                arrowprops=dict(arrowstyle="->", color='#7f1d1d', lw=1.5),
                fontsize=9.5, weight='bold', color='#7f1d1d',
                bbox=dict(boxstyle="round,pad=0.4", fc="#fee2e2", ec="#ef4444", lw=1.2))

    ax.set_xlim(1.5, 5.2)
    ax.set_ylim(6.5, 9.2)
    ax.set_xlabel("Lipophilicity / Grease (cLogP) -> Lower is Better", fontsize=11, weight='bold', labelpad=8)
    ax.set_ylabel("Target Potency (pIC50) -> Higher is Better", fontsize=11, weight='bold', labelpad=8)
    ax.set_title("Potency vs. Grease: Identifying True Binding Efficiency", fontsize=13, weight='bold', pad=15)
    ax.legend(loc='lower left', fontsize=8.5, frameon=True, facecolor='white', edgecolor='#cbd5e1')

    output_path = os.path.join(ARTIFACTS_DIR, "sweetspot_quadrant_analysis.png")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_path}")


def plot_selectivity_comparison():
    """Figure 3: Kinase Family Isoform Selectivity Bar Chart (Log Scale)."""
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=200)

    isoforms = ['JAK2\n(Primary Target)', 'JAK1\n(Off-Target)', 'JAK3\n(Off-Target)', 'TYK2\n(Off-Target)']
    x = np.arange(len(isoforms))
    width = 0.26

    # IC50 values in nM (lower bar = stronger inhibition)
    lead_ic50s = [6.2, 280.0, 450.0, 95.0]
    greasy_ic50s = [4.1, 35.0, 52.0, 18.0]
    tox_ic50s = [12.0, 420.0, 680.0, 140.0]

    rects1 = ax.bar(x - width, lead_ic50s, width, label='JAK2-LEAD-001 (Advance [GO])', color='#10b981', edgecolor='#064e3b')
    rects2 = ax.bar(x, greasy_ic50s, width, label='JAK2-GREASY-002 (Pan-JAK Risk [STOP])', color='#f59e0b', edgecolor='#78350f')
    rects3 = ax.bar(x + width, tox_ic50s, width, label='JAK2-TOX-003 (Selective but Toxic [STOP])', color='#ef4444', edgecolor='#7f1d1d')

    ax.set_ylabel('Inhibition IC50 (nM) - Log Scale (Lower = Stronger Hit)', fontsize=11, weight='bold')
    ax.set_title('Kinome Selectivity Profile: Avoiding Immune System Shutdown', fontsize=13, weight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(isoforms, fontsize=10, weight='bold')
    ax.set_yscale('log')
    ax.set_ylim(1, 2000)
    ax.axhspan(1, 20, color='#10b981', alpha=0.1, label='Target Efficacy Zone (< 20 nM)')
    ax.axhspan(200, 2000, color='#3b82f6', alpha=0.08, label='Desired Safety Separation (> 200 nM)')

    # Annotate fold window for Lead
    ax.annotate("45x Window\n(Spares Immune Cells)", xy=(1 - width, 280), xytext=(0.8, 800),
                arrowprops=dict(arrowstyle="->", color='#064e3b', lw=1.2),
                fontsize=8.5, weight='bold', color='#064e3b',
                bbox=dict(boxstyle="round,pad=0.3", fc="#d1fae5", ec="#10b981"))

    # Annotate narrow window for Greasy
    ax.annotate("Only 8.5x Window!\n[Immunosuppressive Risk]", xy=(1, 35), xytext=(1.05, 75),
                arrowprops=dict(arrowstyle="->", color='#78350f', lw=1.2),
                fontsize=8.5, weight='bold', color='#78350f',
                bbox=dict(boxstyle="round,pad=0.3", fc="#fef3c7", ec="#f59e0b"))

    ax.legend(loc='upper right', fontsize=9, frameon=True, facecolor='white', edgecolor='#cbd5e1')

    output_path = os.path.join(ARTIFACTS_DIR, "kinome_selectivity_comparison.png")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_path}")


def plot_screening_funnel():
    """Figure 4: Portfolio Stage-Gate Attrition Funnel."""
    fig, ax = plt.subplots(figsize=(9, 5), dpi=200)

    stages = [
        ("Hit Generation / Virtual Screen", 100, "#3b82f6", "100 Hit Analogs Synthesized & Tested"),
        ("Tier 1: PhysChem & LipE Gate", 38, "#6366f1", "62% Filtered: Excess Grease & MW > 450 Da"),
        ("Tier 2: Kinase Selectivity Gate", 14, "#8b5cf6", "63% Filtered: Pan-JAK Collateral Risk"),
        ("Tier 3: In Vitro ADMET & DILI Gate", 4, "#ec4899", "71% Filtered: Liver Adducts & CYP Liability"),
        ("Tier 4: In Vivo Lead Nomination", 1, "#10b981", "1 Winner (JAK2-LEAD-001) Advances to Animal PK")
    ]

    y_pos = np.arange(len(stages))
    counts = [s[1] for s in stages]
    colors = [s[2] for s in stages]

    bars = ax.barh(y_pos, counts, color=colors, height=0.55, edgecolor='#1e293b', linewidth=1.2)
    ax.set_yticks(y_pos)
    ax.set_yticklabels([s[0] for s in stages], fontsize=10.5, weight='bold')
    ax.invert_yaxis()
    ax.set_xlabel('Active Molecule Candidates Remaining', fontsize=11, weight='bold')
    ax.set_title('Stage-Gate Attrition Funnel: Eliminating Failure Early', fontsize=13, weight='bold', pad=15)
    ax.set_xlim(0, 115)

    for bar, stage in zip(bars, stages):
        width = bar.get_width()
        ax.text(width + 2, bar.get_y() + bar.get_height()/2, f"{width} ({stage[3]})",
                va='center', ha='left', fontsize=9, weight='bold', color='#1e293b')

    output_path = os.path.join(ARTIFACTS_DIR, "screening_attrition_funnel.png")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    plot_radar_comparison()
    plot_sweetspot_quadrant()
    plot_selectivity_comparison()
    plot_screening_funnel()
    print("All executive visual figures successfully created!")
