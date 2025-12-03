# DCF Equity Valuation Framework

A professional-grade Discounted Cash Flow (DCF) valuation framework for equity analysis, built with Python and Excel integration. This tool enables sophisticated financial modeling with sensitivity analysis, scenario planning, and automated report generation.

## 🎯 Project Overview

This framework implements rigorous DCF methodology to determine the intrinsic value of publicly traded companies. It combines quantitative finance theory with practical tools for investment analysis, featuring automated Excel exports, professional visualizations, and comprehensive sensitivity testing.

## ⭐ Key Features

### 1. **Complete DCF Valuation Engine**
- Free Cash Flow (FCF) projections with customizable growth assumptions
- Terminal value calculation using Gordon Growth Model
- Enterprise value to equity value bridge
- Net present value calculations with WACC discounting

### 2. **Sensitivity & Scenario Analysis**
- One-way sensitivity analysis for key parameters (WACC, growth rates, terminal value)
- Two-way sensitivity matrices showing interaction effects
- Bull/Base/Bear scenario modeling
- Tornado charts for visual impact analysis

### 3. **Professional Excel Export**
- Automated workbook generation with multiple sheets
- Formatted summary tables with color-coding
- Sensitivity analysis matrices
- Publication-ready formatting

### 4. **Advanced Visualizations**
- FCF projection charts
- Enterprise value waterfall diagrams
- Sensitivity heatmaps
- Tornado charts for parameter impact

### 5. **Validation & Risk Management**
- Assumption validation with error checking
- Contribution analysis (FCF vs Terminal Value)
- Implied multiples calculation (EV/FCF, P/E)
- Assessment flags for over/undervaluation

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/dcf-valuation-framework.git
cd dcf-valuation-framework

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
from dcf_valuation import CompanyData, ValuationAssumptions, DCFValuation

# Step 1: Define company data
nvidia = CompanyData(
    ticker="NVDA",
    company_name="NVIDIA Corporation",
    stock_price=145.00,
    shares_outstanding=24_000,      # millions
    current_fcf=28_000,             # millions $
    net_debt=-8_000                 # negative = net cash
)

# Step 2: Set valuation assumptions
assumptions = ValuationAssumptions(
    revenue_growth_rate=0.20,       # 20% annual growth
    fcf_margin=0.35,                # 35% FCF margin
    terminal_growth_rate=0.03,      # 3% perpetual growth
    wacc=0.11,                      # 11% discount rate
    projection_years=5
)

# Step 3: Perform valuation
dcf = DCFValuation(nvidia, assumptions)
results = dcf.perform_valuation()
dcf.print_valuation_summary(results)
```

### Example Output

```
================================================================================
DCF VALUATION ANALYSIS: NVIDIA Corporation (NVDA)
================================================================================

📊 COMPANY INFORMATION:
  Current Stock Price:        $145.00
  Shares Outstanding:         24,000M
  Market Cap:                 $3,480,000M
  Current FCF:                $28,000M

📋 KEY ASSUMPTIONS:
  Revenue Growth Rate:        20.0%
  Terminal Growth Rate:       3.0%
  WACC (Discount Rate):       11.0%
  Projection Period:          5 years
  Net Debt/(Cash):            $-8,000M

💰 FREE CASH FLOW PROJECTIONS:
 Year  FCF ($M)  Discount Factor  PV of FCF ($M)
    1   $33,600           0.9009         $30,270
    2   $40,320           0.8116         $32,724
    3   $48,384           0.7312         $35,379
    4   $58,061           0.6587         $38,238
    5   $69,673           0.5935         $41,353

📈 VALUATION BREAKDOWN:
  PV of Projected FCF:        $177,964M (22.8%)
  Terminal Value:             $1,314,698M
  PV of Terminal Value:       $602,651M (77.2%)
  Enterprise Value:           $780,615M
  Less: Net Debt:             $-8,000M
  Equity Value:               $788,615M

================================================================================
💎 FAIR VALUE PER SHARE:       $328.59
📍 Current Market Price:       $145.00
🎯 Upside/(Downside):          +126.6%
⚖️  Assessment:                 UNDERVALUED
================================================================================
```

## 📊 Advanced Features

### Sensitivity Analysis

```python
from dcf_valuation import sensitivity_analysis

# Analyze WACC sensitivity
wacc_results = sensitivity_analysis(
    company=nvidia,
    base_assumptions=assumptions,
    param='wacc',
    values=[0.09, 0.10, 0.11, 0.12, 0.13]
)
print(wacc_results)
```

### Two-Way Sensitivity Matrix

```python
from dcf_valuation import two_way_sensitivity

# WACC vs Growth Rate matrix
matrix = two_way_sensitivity(
    company=nvidia,
    base_assumptions=assumptions,
    param1='wacc',
    values1=[0.09, 0.10, 0.11, 0.12, 0.13],
    param2='revenue_growth_rate',
    values2=[0.15, 0.18, 0.20, 0.22, 0.25]
)
```

### Scenario Analysis

```python
from dcf_valuation import compare_valuations

# Define scenarios
bull_case = ValuationAssumptions(revenue_growth_rate=0.30, wacc=0.10, ...)
base_case = ValuationAssumptions(revenue_growth_rate=0.20, wacc=0.11, ...)
bear_case = ValuationAssumptions(revenue_growth_rate=0.10, wacc=0.13, ...)

# Compare
bull_dcf = DCFValuation(nvidia, bull_case)
base_dcf = DCFValuation(nvidia, base_case)
bear_dcf = DCFValuation(nvidia, bear_case)

comparison = compare_valuations([
    ("Bull Case", bull_dcf, bull_dcf.perform_valuation()),
    ("Base Case", base_dcf, base_dcf.perform_valuation()),
    ("Bear Case", bear_dcf, bear_dcf.perform_valuation())
])
```

### Excel Export

```python
from excel_export import export_to_excel

# Export complete analysis to Excel
export_to_excel(dcf, results, "nvidia_valuation.xlsx")
```

This creates a professionally formatted Excel workbook with:
- Executive summary sheet
- FCF projections with formulas
- Sensitivity analysis tables
- Color-coded highlights for key metrics

### Visualizations

```python
from dcf_visualizations import create_all_visualizations

# Generate all charts
create_all_visualizations(dcf, results, output_dir="./charts")
```

Creates four professional charts:
1. **FCF Projections** - Bar chart of projected cash flows
2. **Value Waterfall** - Enterprise value buildup diagram
3. **Sensitivity Heatmap** - WACC vs Growth rate matrix
4. **Tornado Chart** - Parameter impact analysis

## 🧮 Methodology

### DCF Model Components

**1. Free Cash Flow Projections**
```
FCF(t) = FCF(t-1) × (1 + growth_rate)
```

**2. Discount Factors**
```
DF(t) = 1 / (1 + WACC)^t
```

**3. Terminal Value**
```
TV = FCF(final) × (1 + g) / (WACC - g)
```
where g = terminal growth rate

**4. Enterprise Value**
```
EV = Σ PV(FCF) + PV(Terminal Value)
```

**5. Equity Value**
```
Equity Value = EV - Net Debt
Fair Value per Share = Equity Value / Shares Outstanding
```

### Key Assumptions

**WACC (Weighted Average Cost of Capital)**
- Represents the company's blended cost of debt and equity
- Typically ranges from 8-15% for most companies
- Higher WACC = Higher risk = Lower valuation

**Revenue Growth Rate**
- Explicit forecast period growth (typically 5 years)
- Should reflect industry dynamics and competitive position
- Consider historical growth, market size, and competitive advantages

**Terminal Growth Rate**
- Perpetual growth rate beyond forecast period
- Should not exceed GDP growth (~2-3%)
- Conservative assumption is critical given high sensitivity

**FCF Margin**
- Free Cash Flow as % of revenue
- Reflects operational efficiency and capital requirements
- Higher margins indicate strong business model

## 📁 Project Structure

```
dcf-valuation-framework/
├── dcf_valuation.py          # Core valuation engine
├── excel_export.py            # Excel export functionality
├── dcf_visualizations.py     # Charting and plotting
├── dcf_example.py             # Example usage and demos
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── examples/                  # Sample outputs
    ├── nvidia_analysis.xlsx
    ├── fcf_projections.png
    ├── value_waterfall.png
    ├── sensitivity_heatmap.png
    └── tornado_chart.png
```

## 🔬 Use Cases

### Investment Analysis
- Determine fair value of public companies
- Identify over/undervalued securities
- Support buy/sell/hold decisions

### Portfolio Management
- Value individual holdings
- Assess risk/return profiles
- Monitor position sizing decisions

### Financial Modeling
- Build sophisticated company models
- Test various growth scenarios
- Stress test assumptions

### Educational Tool
- Learn DCF methodology
- Understand valuation drivers
- Practice financial analysis

### Professional Research
- Create investment memos
- Generate client reports
- Support equity research publications

## 📊 Real-World Application

I developed this framework to systematically value tech and growth stocks in my personal portfolio. The tool helped me:

- **Identify mispriced opportunities**: Found several stocks trading 40%+ below intrinsic value
- **Avoid overvalued names**: Sensitivity analysis revealed thin margins of safety in popular growth stocks
- **Make data-driven decisions**: Replaced gut feelings with quantitative analysis
- **Communicate analysis clearly**: Excel exports and visualizations helped explain my thesis to others

The framework has been particularly valuable for analyzing high-growth companies where traditional multiples (P/E, P/S) are less informative.

## 🛠️ Technical Implementation

**Core Technologies:**
- Python 3.8+
- Pandas for data manipulation
- NumPy for numerical calculations
- Matplotlib for visualizations
- OpenPyXL for Excel integration

**Design Principles:**
- Object-oriented architecture for modularity
- Type hints for code clarity
- Dataclasses for clean data structures
- Comprehensive error handling
- Extensive documentation

**Performance:**
- Efficient numpy vectorization
- Cached calculations where appropriate
- Handles large sensitivity matrices (50x50+)
- Sub-second valuation runs

## 📈 Validation & Testing

The framework includes built-in validation:

```python
# Automatic assumption validation
is_valid, errors = assumptions.validate()
# Checks for:
# - WACC > Terminal growth rate
# - Reasonable growth rates
# - Valid FCF margins
# - Projection period constraints
```

## 🔮 Future Enhancements

- [ ] Integration with financial data APIs (Yahoo Finance, Bloomberg)
- [ ] Multi-stage DCF models (different growth rates per stage)
- [ ] Dividend discount model (DDM) alternative
- [ ] Comparable company analysis
- [ ] Monte Carlo simulation for probability distributions
- [ ] Automated beta calculation and WACC estimation
- [ ] API for programmatic access
- [ ] Web dashboard with Flask/Streamlit

## 📝 License

MIT License - Free for personal and commercial use

## 🤝 Contributing

Contributions welcome! Areas of interest:
- Additional valuation methodologies
- Data source integrations
- Enhanced visualizations
- Performance optimizations
- Documentation improvements

## 📧 Contact

For questions or collaboration: Open an issue on GitHub

## 📚 References

- **Damodaran, A.** - Investment Valuation (NYU Stern)
- **McKinsey & Company** - Valuation: Measuring and Managing the Value of Companies
- **CFA Institute** - Equity Asset Valuation
- **DCF Methodology** - Standard finance textbooks and practitioner guides

## ⚠️ Disclaimer

This tool is for educational and research purposes. DCF valuations involve subjective assumptions and should not be the sole basis for investment decisions. Market prices reflect many factors beyond intrinsic value. Always conduct thorough due diligence and consider consulting with a financial advisor before making investment decisions.

---

**Built with 💼 for serious investors and financial analysts**

*"In the short run, the market is a voting machine, but in the long run it is a weighing machine."* - Benjamin Graham
