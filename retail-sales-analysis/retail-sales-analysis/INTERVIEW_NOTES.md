# Be ready to explain
- **Why clean first?** The raw file had duplicate rows, missing Segment values, inconsistent name case and stray spaces. I removed duplicates, filled missing Segment with "Unknown", standardised text and parsed dates.
- **Hardest SQL?** Q3 (YoY growth with a CTE + LAG) and Q9 (RANK with PARTITION BY).
- **Main insight?** Profit margin drops from about 25% at no discount to negative above 20% discount.
- **Why Excel too?** SUMIFS formulas give business users a live summary they can filter and audit.
- **Why SQLite?** It needs no server, and the same SQL works in MySQL with small changes (date functions).
- **Honest note:** data is synthetic, built to mirror the Kaggle Superstore structure.
