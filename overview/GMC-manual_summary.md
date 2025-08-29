Global Management Challenge: The Definitive Strategic Playbook
1. The Executive Mandate: The Winning Condition
The singular objective of this simulation is to achieve the highest investment performance by the final quarter. All strategic and operational decisions must ultimately serve this goal.
Investment Performance Defined: This is a comprehensive measure of total shareholder return, calculated as:
The final market valuation of the company (share price × number of shares).
Plus: The cumulative cash value of all dividends paid.
Plus: The total cash value of all shares repurchased.
Less: The total cash cost of all new shares issued.
Game Mechanics:
Structure: The simulation unfolds in quarterly increments. Your team analyzes the Management Report from the "Last Quarter" to make decisions for the "Next Quarter."
Competition: You are in a competitive group where all teams begin with identical companies and histories. Your decisions, and those of your rivals, collectively shape the market each quarter.

2. The Strategic Arena: The Business Environment
Your company manufactures three distinct consumer durable products for three unique markets.
Market	Currency	Sales Channel	Strategic Nuance
European Union (EU)	Euro (€)	Agents	Commission is paid on the value of orders received, motivating aggressive selling.
NAFTA	US Dollar ($)	Distributors	Commission is paid on the value of sales made, meaning distributors fulfill demand you create via marketing.
Internet	US Dollar ($)	Direct (via a single distributor)	Global reach. Success is heavily tied to corporate image and website quality. All financial transactions are in USD.
Economic Factors: The simulation models GDP, unemployment, and interest rates. Critically, the € per $ exchange rate impacts your price competitiveness in the two dollar-denominated markets. All your decisions are made in Euros (€).

3. The Operational Playbook: The Decision Matrix
This section details every decision variable, its purpose, parameters, and key interdependencies.
3.1. Marketing & Sales Decisions
Objective: To generate profitable demand, build a powerful brand, and manage the sales channels effectively.
3.1.1. Market Intelligence
Decision: Information Wanted (for Market Shares) & Business Intelligence (for Competitor Activities)
Strategic Purpose: To make informed decisions by understanding market dynamics and competitor strategies.
Parameters:
Units: yes/no (1/0)
Min/Max: 0 / 1
Default: repeat for Shares, 0 for Activities.
Key Considerations: Investing in intelligence is crucial for competitive pricing, advertising, and R&D strategies.
3.1.2. Product Strategy (The 4 Levers of Quality & Price)
Decision: Product Prices
Strategic Purpose: Sets the unit price for each product in each market. The primary lever for revenue and perceived value.
Parameters: Units: euros (€) | Min: 0 (withdraws product) | Max: 999 | Default: repeat.
Key Considerations: Must be balanced with quality. Exchange rate fluctuations directly impact the final price for NAFTA/Internet customers.
Decision: Assembly Times
Strategic Purpose: Determines the build quality and reliability of products. Longer assembly consumes more skilled labor.
Parameters: Units: minutes | Min: 100 (P1), 150 (P2), 300 (P3) | Max: 999 | Default: repeat.
Key Considerations: Direct trade-off between product quality and production capacity of your skilled workforce.
Decision: Premium Materials
Strategic Purpose: Improves product quality and image by using superior materials.
Parameters: Units: % | Min: 0 | Max: 100 | Default: repeat.
Key Considerations: Significantly increases the cost of materials (spot price + 50%).
Decision: Product Development & Implement Improvement
Strategic Purpose: Drives long-term competitiveness through innovation. A MAJOR improvement can reset market perceptions but makes existing stock obsolete.
Parameters (Development): Units: €'000 | Min: 0 | Max: 99 | Default: repeat.
Parameters (Implement): Units: yes/no (1/0) | Min: 0 | Max: 1 | Default: 0.
Key Considerations: Implementing a MAJOR improvement requires careful timing to minimize inventory write-offs.
3.1.3. Promotion & Brand Building
Decision: Advertising (Corporate & Product-Specific)
Strategic Purpose: Drives short-term sales (product) and long-term brand equity (corporate). Corporate image is vital for internet sales.
Parameters: Units: €'000 | Min: 0 | Max: 99 | Default: repeat.
3.1.4. Channel Management
Decision: Agents/distributors wanted, Support Payment, Commission Rate
Strategic Purpose: To build and motivate an effective sales network in the EU and NAFTA.
Parameters (Wanted): Units: number | Min: 0 | Max: 99 | Default: repeat.
Parameters (Support): Units: €'000 | Min: 5 | Max: 99 | Default: repeat.
Parameters (Commission): Units: % | Min: 0 | Max: 99 | Default: repeat.
Key Considerations: High commission and support are needed to attract and retain agents, but they increase your cost of sales.
3.1.5. Internet Presence
Decision: Internet Ports & Website Development
Strategic Purpose: To establish and enhance your direct-to-consumer channel. Capacity must meet peak demand to avoid damaging your brand image.
Parameters (Ports): Units: number | Min: 0 | Max: 99 | Default: repeat.
Parameters (Development): Units: €'000 | Min: 0 | Max: 999 | Default: repeat.
Key Considerations: Website development spending directly correlates to "Star Ratings." Insufficient ports will lead to lost sales.
3.2. Operations & Production Decisions
Objective: To efficiently manufacture and deliver the right quantity of products at the specified quality level.
Decision: Delivery to Europe/Nafta/Internet
Strategic Purpose: Sets the master production schedule for the factory.
Parameters: Units: number | Min: -999 (to return stock) | Max: 9999 | Default: repeat.
Decision: Subcontracting
Strategic Purpose: To supplement in-house component production.
Parameters: Units: number | Min: 0 | Max: 9999 | Default: 0.
Key Considerations: CRITICAL: Subcontracted components have a two-quarter lead time. This requires long-range forecasting.
Decision: Shift Level
Strategic Purpose: To control machine shop capacity. More shifts dramatically increase potential machine hours but also increase unskilled labor costs.
Parameters: Units: number (level) | Min: 1 | Max: 3 | Default: repeat.
Decision: Materials to buy
Strategic Purpose: To manage raw material inventory and cost. Futures market allows for hedging against price volatility.
Parameters: Units: '000 | Min: 0 | Max: 99 | Default: 0.
Key Considerations: Materials are priced in USD, introducing exchange rate risk.
Decision: Machines to buy or sell, Factory - build, Plant maintenance/machine
Strategic Purpose: To manage the physical asset base and its reliability.
Parameters (Machines): Units: number | Min: 0 | Max: 99 | Default: 0.
Parameters (Factory): Units: sq. m. | Min: 0 | Max: 9999 | Default: 0.
Parameters (Maintenance): Units: hours | Min: 0 | Max: 99 | Default: repeat.
3.3. Personnel & Human Resources Decisions
Objective: To ensure the right number of skilled, motivated employees are available to meet production needs.
Decision: Assembly workers to recruit & Assembly workers to train
Strategic Purpose: To manage the size of your critical skilled workforce. Recruiting is uncertain; training is guaranteed but more expensive.
Parameters (Recruit): Units: number | Min: -9 (dismissal) | Max: 99 | Default: 0.
Parameters (Train): Units: number | Min: 0 | Max: 9 | Default: 0.
Decision: Assembly wage rate per hour
Strategic Purpose: Key lever for attracting and retaining skilled workers.
Parameters: Units: cents | Min: 900 | Max: 9999 | Default: repeat.
Key Considerations: This rate can never be decreased. Increases are permanent.
Decision: Management budget & Staff training consultant
Strategic Purpose: To invest in the overall quality of management and employee morale/effectiveness.
Parameters (Budget): Units: €'000 | Min: 30 | Max: 999 | Default: repeat.
Parameters (Training): Units: days | Min: 0 | Max: 60 | Default: repeat.
3.4. Finance & Corporate Strategy Decisions
Objective: To optimize the company's financial structure to support growth and maximize shareholder value.
Decision: Share issue/repurchase & Dividend to pay
Strategic Purpose: To manage the company's equity and directly influence investment performance.
Parameters (Shares): Units: number of shares | Min: -999 | Max: 999 | Default: 0.
Parameters (Dividend): Units: % of share capital | Min: 0 | Max: 99 | Default: 0.
Key Considerations: Dividends are a direct return to shareholders. Share repurchases can increase earnings per share. Both are limited by the company's financial health.
Decision: Additional loan & Term deposit
Strategic Purpose: To manage debt and cash. Taking loans funds expansion but incurs interest costs. Deposits earn interest on idle cash.
Parameters (Loan): Units: €'000 | Min: 0 | Max: 9999 | Default: 0.
Parameters (Deposit): Units: €'000 | Min: -999 | Max: 9999 | Default: 0.
Decision: Insurance plan
Strategic Purpose: To mitigate the financial impact of random disruptive events.
Parameters: Units: number (plan) | Min: 0 | Max: 4 | Default: repeat.
Key Considerations: A classic risk vs. cost trade-off. No insurance (Plan 0) exposes the company to full financial liability from insurable events.

4. The Intelligence Briefing: Deconstructing the Management Report
Your quarterly report is your primary source of feedback and data.
Part 1: Your Company: Analyze your performance in detail.
Decisions: Check for * which indicates the simulator altered your decision due to a constraint (e.g., lack of funds, insufficient labor).
Financials: The Income Statement, Balance Sheet, and Cash Flow are the ultimate scorecards of your operational efficiency and profitability.
Key Metrics: Pay close attention to machine efficiency, employee turnover, product stock levels, and order backlogs.
Part 2: Group & Economic Information: Understand the external environment.
Competitor Data: Use the intelligence reports to benchmark your performance and anticipate rival moves.
Economic Intelligence: Use the GDP, unemployment, and exchange rate data to forecast market trends.
Business Report: This is critical reading. It contains qualitative information and hints about potential market shifts or "world events" that are not reflected in the quantitative data.
