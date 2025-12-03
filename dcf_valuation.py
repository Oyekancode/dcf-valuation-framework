"""
DCF Valuation Framework
=======================
Professional-grade Discounted Cash Flow valuation tool for equity analysis.
"""

import pandas as pd
import numpy as np
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple, Optional
from datetime import datetime


@dataclass
class CompanyData:
    """Company financial data and assumptions"""
    ticker: str
    company_name: str
    stock_price: float
    shares_outstanding: float  # in millions
    current_fcf: float  # in millions
    net_debt: float  # in millions (positive = debt, negative = net cash)
    
    def market_cap(self) -> float:
        """Calculate current market capitalization"""
        return self.stock_price * self.shares_outstanding
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class ValuationAssumptions:
    """DCF model assumptions"""
    revenue_growth_rate: float
    fcf_margin: float  # For revenue-based projections
    terminal_growth_rate: float
    wacc: float  # Weighted Average Cost of Capital
    projection_years: int = 5
    
    def validate(self) -> Tuple[bool, List[str]]:
        """Validate assumptions for reasonableness"""
        errors = []
        
        if self.revenue_growth_rate < -0.5 or self.revenue_growth_rate > 1.0:
            errors.append("Revenue growth rate should be between -50% and 100%")
        
        if self.terminal_growth_rate < 0 or self.terminal_growth_rate > 0.05:
            errors.append("Terminal growth rate should be between 0% and 5%")
        
        if self.wacc <= self.terminal_growth_rate:
            errors.append("WACC must be greater than terminal growth rate")
        
        if self.fcf_margin < 0 or self.fcf_margin > 1.0:
            errors.append("FCF margin should be between 0% and 100%")
        
        return len(errors) == 0, errors
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return asdict(self)


class DCFValuation:
    """Performs DCF valuation calculations with advanced features"""

    def __init__(self, company: CompanyData, assumptions: ValuationAssumptions):
        self.company = company
        self.assumptions = assumptions
        self.validation_date = datetime.now()
        
        # Validate assumptions
        is_valid, errors = self.assumptions.validate()
        if not is_valid:
            print("⚠️  Warning: Assumption validation issues:")
            for error in errors:
                print(f"  - {error}")
            print()

    def calculate_discount_factors(self) -> List[float]:
        """Calculate discount factors for each year"""
        years = range(1, self.assumptions.projection_years + 1)
        return [1 / (1 + self.assumptions.wacc) ** year for year in years]

    def project_fcf(self) -> List[float]:
        """Project free cash flows for explicit forecast period"""
        fcf_projections = [self.company.current_fcf]

        for year in range(1, self.assumptions.projection_years + 1):
            next_fcf = fcf_projections[-1] * (1 + self.assumptions.revenue_growth_rate)
            fcf_projections.append(next_fcf)

        return fcf_projections[1:]  # Exclude base year

    def calculate_terminal_value(self, terminal_fcf: float) -> float:
        """Calculate terminal value using perpetuity growth method"""
        return terminal_fcf * (1 + self.assumptions.terminal_growth_rate) / \
               (self.assumptions.wacc - self.assumptions.terminal_growth_rate)

    def calculate_pv_of_fcf(self, fcf_projections: List[float],
                           discount_factors: List[float]) -> List[float]:
        """Calculate present value of projected free cash flows"""
        return [fcf * df for fcf, df in zip(fcf_projections, discount_factors)]

    def perform_valuation(self) -> Dict:
        """Perform complete DCF valuation"""
        # Project FCF
        fcf_projections = self.project_fcf()

        # Calculate discount factors
        discount_factors = self.calculate_discount_factors()

        # Calculate PV of FCF
        pv_fcf = self.calculate_pv_of_fcf(fcf_projections, discount_factors)

        # Calculate terminal value
        terminal_fcf = fcf_projections[-1]
        terminal_value = self.calculate_terminal_value(terminal_fcf)
        pv_terminal_value = terminal_value * discount_factors[-1]

        # Calculate enterprise and equity value
        pv_fcf_sum = sum(pv_fcf)
        enterprise_value = pv_fcf_sum + pv_terminal_value
        equity_value = enterprise_value - self.company.net_debt

        # Calculate per share values
        fair_value_per_share = equity_value / self.company.shares_outstanding
        upside_downside = (fair_value_per_share - self.company.stock_price) / \
                         self.company.stock_price

        # Calculate implied metrics
        ev_to_fcf = enterprise_value / self.company.current_fcf if self.company.current_fcf > 0 else None
        pe_implied = self.company.market_cap() / (self.company.current_fcf * 0.8) if self.company.current_fcf > 0 else None
        
        # Calculate contribution percentages
        fcf_contribution = pv_fcf_sum / enterprise_value if enterprise_value > 0 else 0
        terminal_contribution = pv_terminal_value / enterprise_value if enterprise_value > 0 else 0

        return {
            'fcf_projections': fcf_projections,
            'discount_factors': discount_factors,
            'pv_fcf': pv_fcf,
            'terminal_value': terminal_value,
            'pv_terminal_value': pv_terminal_value,
            'pv_fcf_sum': pv_fcf_sum,
            'enterprise_value': enterprise_value,
            'equity_value': equity_value,
            'fair_value_per_share': fair_value_per_share,
            'current_price': self.company.stock_price,
            'upside_downside_pct': upside_downside * 100,
            'assessment': 'UNDERVALUED' if upside_downside > 0 else 'OVERVALUED',
            'ev_to_fcf': ev_to_fcf,
            'implied_pe': pe_implied,
            'fcf_contribution_pct': fcf_contribution * 100,
            'terminal_contribution_pct': terminal_contribution * 100
        }

    def create_summary_table(self, results: Dict) -> pd.DataFrame:
        """Create a formatted summary table of results"""
        years = list(range(1, self.assumptions.projection_years + 1))

        df = pd.DataFrame({
            'Year': years,
            'FCF ($M)': [f"${x:,.0f}" for x in results['fcf_projections']],
            'Discount Factor': [f"{x:.4f}" for x in results['discount_factors']],
            'PV of FCF ($M)': [f"${x:,.0f}" for x in results['pv_fcf']]
        })

        return df

    def create_detailed_dataframe(self, results: Dict) -> pd.DataFrame:
        """Create detailed DataFrame for export"""
        years = list(range(1, self.assumptions.projection_years + 1))
        
        df = pd.DataFrame({
            'Year': years,
            'FCF_Projection': results['fcf_projections'],
            'Discount_Factor': results['discount_factors'],
            'PV_FCF': results['pv_fcf'],
            'Growth_Rate': [self.assumptions.revenue_growth_rate] * len(years)
        })
        
        return df

    def print_valuation_summary(self, results: Dict):
        """Print formatted valuation summary"""
        print(f"\n{'='*80}")
        print(f"DCF VALUATION ANALYSIS: {self.company.company_name} ({self.company.ticker})")
        print(f"{'='*80}\n")

        print("📊 COMPANY INFORMATION:")
        print(f"  Current Stock Price:        ${self.company.stock_price:,.2f}")
        print(f"  Shares Outstanding:         {self.company.shares_outstanding:,.0f}M")
        print(f"  Market Cap:                 ${self.company.market_cap():,.0f}M")
        print(f"  Current FCF:                ${self.company.current_fcf:,.0f}M")

        print("\n📋 KEY ASSUMPTIONS:")
        print(f"  Revenue Growth Rate:        {self.assumptions.revenue_growth_rate*100:.1f}%")
        print(f"  Terminal Growth Rate:       {self.assumptions.terminal_growth_rate*100:.1f}%")
        print(f"  WACC (Discount Rate):       {self.assumptions.wacc*100:.1f}%")
        print(f"  Projection Period:          {self.assumptions.projection_years} years")
        print(f"  Net Debt/(Cash):            ${self.company.net_debt:,.0f}M")

        print("\n💰 FREE CASH FLOW PROJECTIONS:")
        print(self.create_summary_table(results).to_string(index=False))

        print("\n📈 VALUATION BREAKDOWN:")
        print(f"  PV of Projected FCF:        ${results['pv_fcf_sum']:,.0f}M ({results['fcf_contribution_pct']:.1f}%)")
        print(f"  Terminal Value:             ${results['terminal_value']:,.0f}M")
        print(f"  PV of Terminal Value:       ${results['pv_terminal_value']:,.0f}M ({results['terminal_contribution_pct']:.1f}%)")
        print(f"  Enterprise Value:           ${results['enterprise_value']:,.0f}M")
        print(f"  Less: Net Debt:             ${self.company.net_debt:,.0f}M")
        print(f"  Equity Value:               ${results['equity_value']:,.0f}M")

        print(f"\n{'='*80}")
        print(f"💎 FAIR VALUE PER SHARE:       ${results['fair_value_per_share']:,.2f}")
        print(f"📍 Current Market Price:       ${results['current_price']:,.2f}")
        print(f"🎯 Upside/(Downside):          {results['upside_downside_pct']:+.1f}%")
        print(f"⚖️  Assessment:                 {results['assessment']}")
        print(f"{'='*80}\n")
        
        # Additional metrics
        if results['ev_to_fcf']:
            print(f"📊 EV/FCF Multiple:            {results['ev_to_fcf']:.2f}x")
        
        print(f"📅 Valuation Date:             {self.validation_date.strftime('%Y-%m-%d %H:%M')}")
        print()


def sensitivity_analysis(company: CompanyData, base_assumptions: ValuationAssumptions,
                        param: str, values: List[float]) -> pd.DataFrame:
    """
    Perform sensitivity analysis on a parameter

    Args:
        company: Company data
        base_assumptions: Base case assumptions
        param: Parameter to vary ('wacc', 'revenue_growth_rate', 'terminal_growth_rate')
        values: List of values to test
    """
    results = []

    for value in values:
        # Create new assumptions with modified parameter
        assumptions = ValuationAssumptions(
            revenue_growth_rate=base_assumptions.revenue_growth_rate,
            fcf_margin=base_assumptions.fcf_margin,
            terminal_growth_rate=base_assumptions.terminal_growth_rate,
            wacc=base_assumptions.wacc,
            projection_years=base_assumptions.projection_years
        )

        # Modify the specific parameter
        setattr(assumptions, param, value)

        # Run valuation
        dcf = DCFValuation(company, assumptions)
        valuation_results = dcf.perform_valuation()

        results.append({
            param: f"{value*100:.1f}%",
            'Fair Value': f"${valuation_results['fair_value_per_share']:.2f}",
            'Upside/(Downside)': f"{valuation_results['upside_downside_pct']:+.1f}%",
            'Assessment': valuation_results['assessment']
        })

    return pd.DataFrame(results)


def two_way_sensitivity(company: CompanyData, base_assumptions: ValuationAssumptions,
                       param1: str, values1: List[float],
                       param2: str, values2: List[float]) -> pd.DataFrame:
    """
    Perform two-way sensitivity analysis
    
    Args:
        company: Company data
        base_assumptions: Base case assumptions
        param1: First parameter to vary
        values1: Values for first parameter
        param2: Second parameter to vary
        values2: Values for second parameter
    
    Returns:
        DataFrame with sensitivity matrix
    """
    results = []
    
    for val1 in values1:
        row = {f'{param1}': f"{val1*100:.1f}%"}
        
        for val2 in values2:
            assumptions = ValuationAssumptions(
                revenue_growth_rate=base_assumptions.revenue_growth_rate,
                fcf_margin=base_assumptions.fcf_margin,
                terminal_growth_rate=base_assumptions.terminal_growth_rate,
                wacc=base_assumptions.wacc,
                projection_years=base_assumptions.projection_years
            )
            
            setattr(assumptions, param1, val1)
            setattr(assumptions, param2, val2)
            
            dcf = DCFValuation(company, assumptions)
            valuation_results = dcf.perform_valuation()
            
            row[f"{val2*100:.1f}%"] = f"${valuation_results['fair_value_per_share']:.2f}"
        
        results.append(row)
    
    return pd.DataFrame(results)


def compare_valuations(valuations: List[Tuple[str, DCFValuation, Dict]]) -> pd.DataFrame:
    """
    Compare multiple valuations side by side
    
    Args:
        valuations: List of tuples (scenario_name, dcf_object, results_dict)
    
    Returns:
        Comparison DataFrame
    """
    comparison_data = []
    
    for scenario_name, dcf, results in valuations:
        comparison_data.append({
            'Scenario': scenario_name,
            'Fair Value': f"${results['fair_value_per_share']:.2f}",
            'Upside/(Downside)': f"{results['upside_downside_pct']:+.1f}%",
            'Enterprise Value': f"${results['enterprise_value']:,.0f}M",
            'Terminal Value %': f"{results['terminal_contribution_pct']:.1f}%",
            'Assessment': results['assessment']
        })
    
    return pd.DataFrame(comparison_data)
