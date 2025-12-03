"""
Visualization Module for DCF Analysis
=====================================
Create professional charts and visualizations for DCF valuations
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from dcf_valuation import DCFValuation, CompanyData, ValuationAssumptions, sensitivity_analysis


def plot_fcf_projections(dcf: DCFValuation, results: Dict, save_path: str = None):
    """
    Plot FCF projections and present values
    
    Args:
        dcf: DCFValuation object
        results: Valuation results
        save_path: Optional path to save figure
    """
    years = list(range(1, dcf.assumptions.projection_years + 1))
    fcf = results['fcf_projections']
    pv_fcf = results['pv_fcf']
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # FCF Projections
    ax1.bar(years, fcf, color='#366092', alpha=0.8, label='Projected FCF')
    ax1.set_xlabel('Year', fontsize=11)
    ax1.set_ylabel('Free Cash Flow ($M)', fontsize=11)
    ax1.set_title(f'FCF Projections - {dcf.company.ticker}', fontsize=12, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    ax1.legend()
    
    # Format y-axis
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}M'))
    
    # PV of FCF
    colors = ['#366092' if i < len(years) else '#FF6B6B' for i in range(len(years) + 1)]
    all_values = pv_fcf + [results['pv_terminal_value']]
    labels = [f'Year {y}' for y in years] + ['Terminal\nValue']
    
    bars = ax2.bar(range(len(all_values)), all_values, color=colors, alpha=0.8)
    ax2.set_xlabel('Period', fontsize=11)
    ax2.set_ylabel('Present Value ($M)', fontsize=11)
    ax2.set_title('Present Value Breakdown', fontsize=12, fontweight='bold')
    ax2.set_xticks(range(len(all_values)))
    ax2.set_xticklabels(labels, rotation=45, ha='right')
    ax2.grid(axis='y', alpha=0.3)
    
    # Format y-axis
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}M'))
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'${height:,.0f}M',
                ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Chart saved: {save_path}")
    
    return fig


def plot_value_waterfall(dcf: DCFValuation, results: Dict, save_path: str = None):
    """
    Create waterfall chart showing enterprise value buildup
    
    Args:
        dcf: DCFValuation object
        results: Valuation results
        save_path: Optional path to save figure
    """
    categories = ['PV of FCF', 'Terminal Value', 'Enterprise\nValue', 'Less: Net Debt', 'Equity Value']
    values = [
        results['pv_fcf_sum'],
        results['pv_terminal_value'],
        results['enterprise_value'],
        -dcf.company.net_debt,
        results['equity_value']
    ]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create waterfall effect
    cumulative = [0]
    for i, val in enumerate(values[:-1]):
        cumulative.append(cumulative[-1] + val)
    
    colors = ['#366092', '#4A90E2', '#7CB342', '#FFA726', '#66BB6A']
    
    # Plot bars
    for i, (cat, val) in enumerate(zip(categories, values)):
        if i < len(cumulative) - 1:
            bottom = cumulative[i]
            ax.bar(i, val, bottom=bottom, color=colors[i], alpha=0.8, edgecolor='black')
            
            # Add value labels
            ax.text(i, bottom + val/2, f'${val:,.0f}M', 
                   ha='center', va='center', fontweight='bold', fontsize=9)
        else:
            # Final bar (equity value)
            ax.bar(i, val, color=colors[i], alpha=0.8, edgecolor='black')
            ax.text(i, val/2, f'${val:,.0f}M', 
                   ha='center', va='center', fontweight='bold', fontsize=9)
    
    ax.set_xticks(range(len(categories)))
    ax.set_xticklabels(categories)
    ax.set_ylabel('Value ($M)', fontsize=11)
    ax.set_title(f'Enterprise Value Waterfall - {dcf.company.ticker}', 
                fontsize=12, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    
    # Format y-axis
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}M'))
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Chart saved: {save_path}")
    
    return fig


def plot_sensitivity_heatmap(dcf: DCFValuation, save_path: str = None):
    """
    Create sensitivity heatmap for WACC vs Growth Rate
    
    Args:
        dcf: DCFValuation object
        save_path: Optional path to save figure
    """
    # Create range of values
    wacc_values = np.linspace(
        max(dcf.assumptions.wacc - 0.03, dcf.assumptions.terminal_growth_rate + 0.01),
        dcf.assumptions.wacc + 0.03, 7
    )
    growth_values = np.linspace(
        max(dcf.assumptions.revenue_growth_rate - 0.10, -0.20),
        dcf.assumptions.revenue_growth_rate + 0.10, 7
    )
    
    # Calculate fair values
    fair_values = np.zeros((len(wacc_values), len(growth_values)))
    
    for i, wacc in enumerate(wacc_values):
        for j, growth in enumerate(growth_values):
            temp_assumptions = ValuationAssumptions(
                revenue_growth_rate=growth,
                fcf_margin=dcf.assumptions.fcf_margin,
                terminal_growth_rate=dcf.assumptions.terminal_growth_rate,
                wacc=wacc,
                projection_years=dcf.assumptions.projection_years
            )
            
            temp_dcf = DCFValuation(dcf.company, temp_assumptions)
            temp_results = temp_dcf.perform_valuation()
            fair_values[i, j] = temp_results['fair_value_per_share']
    
    # Create heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    
    im = ax.imshow(fair_values, cmap='RdYlGn', aspect='auto')
    
    # Set ticks
    ax.set_xticks(np.arange(len(growth_values)))
    ax.set_yticks(np.arange(len(wacc_values)))
    ax.set_xticklabels([f'{v*100:.1f}%' for v in growth_values])
    ax.set_yticklabels([f'{v*100:.1f}%' for v in wacc_values])
    
    # Labels
    ax.set_xlabel('Revenue Growth Rate', fontsize=11)
    ax.set_ylabel('WACC (Discount Rate)', fontsize=11)
    ax.set_title(f'Fair Value Sensitivity Analysis - {dcf.company.ticker}\nCurrent Price: ${dcf.company.stock_price:.2f}', 
                fontsize=12, fontweight='bold')
    
    # Add text annotations
    for i in range(len(wacc_values)):
        for j in range(len(growth_values)):
            text = ax.text(j, i, f'${fair_values[i, j]:.2f}',
                         ha="center", va="center", color="black", fontsize=8)
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Fair Value per Share ($)', rotation=270, labelpad=20)
    
    # Highlight base case
    base_wacc_idx = np.argmin(np.abs(wacc_values - dcf.assumptions.wacc))
    base_growth_idx = np.argmin(np.abs(growth_values - dcf.assumptions.revenue_growth_rate))
    ax.add_patch(plt.Rectangle((base_growth_idx-0.5, base_wacc_idx-0.5), 1, 1,
                              fill=False, edgecolor='blue', linewidth=3))
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Chart saved: {save_path}")
    
    return fig


def plot_tornado_chart(dcf: DCFValuation, results: Dict, save_path: str = None):
    """
    Create tornado chart showing impact of parameter changes
    
    Args:
        dcf: DCFValuation object
        results: Base case results
        save_path: Optional path to save figure
    """
    base_fair_value = results['fair_value_per_share']
    
    parameters = {
        'WACC': ('wacc', [-0.02, +0.02]),
        'Growth Rate': ('revenue_growth_rate', [-0.05, +0.05]),
        'Terminal Growth': ('terminal_growth_rate', [-0.01, +0.01]),
        'Current FCF': ('current_fcf', [-0.20, +0.20])
    }
    
    impacts = []
    
    for param_name, (param_key, changes) in parameters.items():
        low_values = []
        high_values = []
        
        for change in changes:
            temp_company = CompanyData(
                ticker=dcf.company.ticker,
                company_name=dcf.company.company_name,
                stock_price=dcf.company.stock_price,
                shares_outstanding=dcf.company.shares_outstanding,
                current_fcf=dcf.company.current_fcf,
                net_debt=dcf.company.net_debt
            )
            
            temp_assumptions = ValuationAssumptions(
                revenue_growth_rate=dcf.assumptions.revenue_growth_rate,
                fcf_margin=dcf.assumptions.fcf_margin,
                terminal_growth_rate=dcf.assumptions.terminal_growth_rate,
                wacc=dcf.assumptions.wacc,
                projection_years=dcf.assumptions.projection_years
            )
            
            if param_key == 'current_fcf':
                temp_company.current_fcf *= (1 + change)
            else:
                current_val = getattr(temp_assumptions, param_key)
                setattr(temp_assumptions, param_key, current_val + change)
            
            temp_dcf = DCFValuation(temp_company, temp_assumptions)
            temp_results = temp_dcf.perform_valuation()
            
            if change < 0:
                low_values.append(temp_results['fair_value_per_share'])
            else:
                high_values.append(temp_results['fair_value_per_share'])
        
        low_impact = base_fair_value - low_values[0]
        high_impact = high_values[0] - base_fair_value
        impacts.append((param_name, low_impact, high_impact))
    
    # Sort by total impact
    impacts.sort(key=lambda x: abs(x[1]) + abs(x[2]), reverse=True)
    
    # Create plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    y_pos = np.arange(len(impacts))
    
    for i, (param, low, high) in enumerate(impacts):
        # Low impact (left bar)
        ax.barh(i, -low, left=base_fair_value-low, height=0.7, 
               color='#E57373', alpha=0.8)
        # High impact (right bar)
        ax.barh(i, high, left=base_fair_value, height=0.7, 
               color='#81C784', alpha=0.8)
    
    # Base case line
    ax.axvline(base_fair_value, color='black', linestyle='--', linewidth=2, label='Base Case')
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels([imp[0] for imp in impacts])
    ax.set_xlabel('Fair Value per Share ($)', fontsize=11)
    ax.set_title(f'Tornado Chart: Sensitivity to Key Parameters - {dcf.company.ticker}', 
                fontsize=12, fontweight='bold')
    ax.legend()
    ax.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Chart saved: {save_path}")
    
    return fig


def create_all_visualizations(dcf: DCFValuation, results: Dict, output_dir: str = "."):
    """
    Generate all visualization charts
    
    Args:
        dcf: DCFValuation object
        results: Valuation results
        output_dir: Directory to save charts
    """
    import os
    
    print("\n📊 Generating visualizations...")
    
    # FCF Projections
    plot_fcf_projections(dcf, results, f"{output_dir}/fcf_projections.png")
    
    # Waterfall Chart
    plot_value_waterfall(dcf, results, f"{output_dir}/value_waterfall.png")
    
    # Sensitivity Heatmap
    plot_sensitivity_heatmap(dcf, f"{output_dir}/sensitivity_heatmap.png")
    
    # Tornado Chart
    plot_tornado_chart(dcf, results, f"{output_dir}/tornado_chart.png")
    
    print("✓ All visualizations generated!\n")
    
    plt.close('all')
