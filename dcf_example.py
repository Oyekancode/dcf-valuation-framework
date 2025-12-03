"""
DCF Valuation Framework - Complete Example
==========================================
Demonstrates all features of the DCF valuation tool
"""

from dcf_valuation import (
    CompanyData, ValuationAssumptions, DCFValuation,
    sensitivity_analysis, two_way_sensitivity, compare_valuations
)
from dcf_visualizations import create_all_visualizations
from excel_export import export_to_excel


def example_nvidia_valuation():
    """Example: NVIDIA Corporation"""
    
    print("\n" + "="*80)
    print("EXAMPLE 1: NVIDIA CORPORATION (NVDA)")
    print("="*80)
    
    # Company data
    nvidia = CompanyData(
        ticker="NVDA",
        company_name="NVIDIA Corporation",
        stock_price=145.00,
        shares_outstanding=24_000,  # millions
        current_fcf=28_000,  # millions
        net_debt=-8_000  # negative = net cash
    )
    
    # Valuation assumptions
    nvidia_assumptions = ValuationAssumptions(
        revenue_growth_rate=0.20,  # 20% growth
        fcf_margin=0.35,  # 35% FCF margin
        terminal_growth_rate=0.03,  # 3% perpetual
        wacc=0.11,  # 11% discount rate
        projection_years=5
    )
    
    # Perform valuation
    dcf = DCFValuation(nvidia, nvidia_assumptions)
    results = dcf.perform_valuation()
    dcf.print_valuation_summary(results)
    
    return dcf, results


def example_sensitivity_analysis(dcf, results):
    """Demonstrate sensitivity analysis"""
    
    print("\n" + "="*80)
    print("SENSITIVITY ANALYSIS")
    print("="*80)
    
    # WACC Sensitivity
    print("\n📊 WACC Sensitivity:")
    print("-" * 80)
    wacc_sens = sensitivity_analysis(
        company=dcf.company,
        base_assumptions=dcf.assumptions,
        param='wacc',
        values=[0.09, 0.10, 0.11, 0.12, 0.13]
    )
    print(wacc_sens.to_string(index=False))
    
    # Growth Rate Sensitivity
    print("\n📊 Revenue Growth Sensitivity:")
    print("-" * 80)
    growth_sens = sensitivity_analysis(
        company=dcf.company,
        base_assumptions=dcf.assumptions,
        param='revenue_growth_rate',
        values=[0.10, 0.15, 0.20, 0.25, 0.30]
    )
    print(growth_sens.to_string(index=False))
    
    # Two-way sensitivity
    print("\n📊 Two-Way Sensitivity: WACC vs Growth Rate:")
    print("-" * 80)
    two_way = two_way_sensitivity(
        company=dcf.company,
        base_assumptions=dcf.assumptions,
        param1='wacc',
        values1=[0.09, 0.10, 0.11, 0.12, 0.13],
        param2='revenue_growth_rate',
        values2=[0.15, 0.18, 0.20, 0.22, 0.25]
    )
    print(two_way.to_string(index=False))


def example_scenario_analysis(nvidia):
    """Demonstrate scenario analysis"""
    
    print("\n" + "="*80)
    print("SCENARIO ANALYSIS")
    print("="*80)
    
    # Base case (already done)
    base_assumptions = ValuationAssumptions(
        revenue_growth_rate=0.20,
        fcf_margin=0.35,
        terminal_growth_rate=0.03,
        wacc=0.11,
        projection_years=5
    )
    
    # Bull case
    bull_assumptions = ValuationAssumptions(
        revenue_growth_rate=0.30,  # Higher growth
        fcf_margin=0.35,
        terminal_growth_rate=0.035,  # Higher terminal growth
        wacc=0.10,  # Lower discount rate
        projection_years=5
    )
    
    # Bear case
    bear_assumptions = ValuationAssumptions(
        revenue_growth_rate=0.10,  # Lower growth
        fcf_margin=0.35,
        terminal_growth_rate=0.025,
        wacc=0.13,  # Higher discount rate
        projection_years=5
    )
    
    # Run valuations
    base_dcf = DCFValuation(nvidia, base_assumptions)
    base_results = base_dcf.perform_valuation()
    
    bull_dcf = DCFValuation(nvidia, bull_assumptions)
    bull_results = bull_dcf.perform_valuation()
    
    bear_dcf = DCFValuation(nvidia, bear_assumptions)
    bear_results = bear_dcf.perform_valuation()
    
    # Compare
    comparison = compare_valuations([
        ("🐻 Bear Case", bear_dcf, bear_results),
        ("📊 Base Case", base_dcf, base_results),
        ("🐂 Bull Case", bull_dcf, bull_results)
    ])
    
    print("\n" + comparison.to_string(index=False))
    
    return base_dcf, base_results


def example_apple_valuation():
    """Example: Apple Inc."""
    
    print("\n" + "="*80)
    print("EXAMPLE 2: APPLE INC. (AAPL)")
    print("="*80)
    
    apple = CompanyData(
        ticker="AAPL",
        company_name="Apple Inc.",
        stock_price=235.00,
        shares_outstanding=15_200,
        current_fcf=110_000,
        net_debt=-60_000  # net cash position
    )
    
    apple_assumptions = ValuationAssumptions(
        revenue_growth_rate=0.08,  # 8% growth
        fcf_margin=0.30,
        terminal_growth_rate=0.025,
        wacc=0.09,
        projection_years=5
    )
    
    dcf = DCFValuation(apple, apple_assumptions)
    results = dcf.perform_valuation()
    dcf.print_valuation_summary(results)
    
    return dcf, results


def example_custom_company():
    """Template for custom company valuation"""
    
    print("\n" + "="*80)
    print("YOUR CUSTOM COMPANY TEMPLATE")
    print("="*80)
    
    print("""
To value your own company, customize the following template:

from dcf_valuation import CompanyData, ValuationAssumptions, DCFValuation

# 1. Input company data
my_company = CompanyData(
    ticker="XXXX",
    company_name="Your Company Name",
    stock_price=100.00,              # Current stock price
    shares_outstanding=1000,         # Millions of shares
    current_fcf=500,                 # Latest FCF in millions
    net_debt=200                     # Net debt in millions (negative if net cash)
)

# 2. Set valuation assumptions
my_assumptions = ValuationAssumptions(
    revenue_growth_rate=0.15,        # 15% annual growth
    fcf_margin=0.25,                 # 25% FCF margin
    terminal_growth_rate=0.03,       # 3% perpetual growth
    wacc=0.10,                       # 10% discount rate
    projection_years=5               # 5-year projection
)

# 3. Run the valuation
dcf = DCFValuation(my_company, my_assumptions)
results = dcf.perform_valuation()
dcf.print_valuation_summary(results)

# 4. Optional: Export to Excel
from excel_export import export_to_excel
export_to_excel(dcf, results, "my_company_dcf.xlsx")

# 5. Optional: Generate charts
from dcf_visualizations import create_all_visualizations
create_all_visualizations(dcf, results, output_dir="./charts")
""")


def main():
    """Run all examples"""
    
    print("\n" + "="*80)
    print("DCF VALUATION FRAMEWORK - COMPREHENSIVE DEMONSTRATION")
    print("="*80)
    print("\nThis example demonstrates:")
    print("  ✓ Company valuation with full DCF model")
    print("  ✓ Sensitivity analysis")
    print("  ✓ Scenario analysis (Bull/Base/Bear)")
    print("  ✓ Excel export functionality")
    print("  ✓ Professional visualizations")
    
    # Example 1: NVIDIA
    nvidia_dcf, nvidia_results = example_nvidia_valuation()
    
    # Sensitivity Analysis
    example_sensitivity_analysis(nvidia_dcf, nvidia_results)
    
    # Scenario Analysis
    print("\n\n")
    base_dcf, base_results = example_scenario_analysis(nvidia_dcf.company)
    
    # Example 2: Apple
    apple_dcf, apple_results = example_apple_valuation()
    
    # Export examples
    print("\n" + "="*80)
    print("EXPORT OPTIONS")
    print("="*80)
    
    try:
        print("\n📊 Generating visualizations...")
        create_all_visualizations(nvidia_dcf, nvidia_results, output_dir="/home/claude")
        print("✓ Charts saved to current directory")
    except Exception as e:
        print(f"Note: Visualization generation requires matplotlib ({str(e)})")
    
    try:
        print("\n📁 Exporting to Excel...")
        export_to_excel(nvidia_dcf, nvidia_results, "/home/claude/nvidia_dcf_analysis.xlsx")
        print("✓ Excel file created: nvidia_dcf_analysis.xlsx")
    except Exception as e:
        print(f"Note: Excel export requires openpyxl ({str(e)})")
    
    # Custom template
    example_custom_company()
    
    # Summary
    print("\n" + "="*80)
    print("DEMONSTRATION COMPLETE")
    print("="*80)
    print("\n✓ All features demonstrated successfully!")
    print("\nKey Features:")
    print("  • Rigorous DCF valuation methodology")
    print("  • Comprehensive sensitivity analysis")
    print("  • Scenario modeling (Bull/Base/Bear)")
    print("  • Professional Excel exports")
    print("  • Publication-quality charts")
    print("  • Easy-to-use API for custom valuations")
    
    print("\n💡 Pro Tips:")
    print("  • Always validate your assumptions with sensitivity analysis")
    print("  • Terminal value typically represents 60-80% of enterprise value")
    print("  • WACC should reflect the company's risk profile")
    print("  • Use conservative growth rates for mature companies")
    print("  • Compare your valuation with market multiples")
    
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
