MCM 2026 Problem A involves tracking the change in battery capacity over time and how it affects the total battery life. Reading the literature on this problem (and its analogs for products like electric vehicles) built our intuition that the capacity should be strictly monotone along with the battery life.

Meeting the deliverables of Problem A mainly entails three models: the State of Charge (SOC) over Time, Time To Empty (TTE) over SOC, and the Power Drain Function (also called Discharge Rate, PDF). Initial research led to a decay model as our SOC and a logistic model as our baseline TTE. These were aligned only with general research figures and not deterministic functions.

We backed our next approach with battery loss data from the collated Sherlock Lithium Ion Battery dataset by introducing stochastic noise into our SOC and TTE functions, creating two SDEs. We ran a Monte Carlo simulation and took the mean result, giving us our second baseline.

We were left with some issues. First, our noise injection wasn't matching the data as well as we wanted because the drift component of the SDE was too inaccurate. We needed a more accurate model built on physical factors. We went back to the simple SOC circuit formula with PDF and noise coefficients. We derived our new TTE from this function as well. This gave us, in theory, better models - but our PDF was still lacking.

For ease of computation, we had started with a constant PDF, then shifted to a weighted function of the physical components of the phone that we saw had a high correlation from the research. Seeing these methods fail as well, we decided to create our own analytic PDF by approximating the function from battery loss rates. 

Combining these results led to a more accurate model based on our data. We also implemented realistic limits in terms of SOC thresholds (learning that phones will shut off after hitting a specific battery threshold), among other constraints.

We then shifted our attention to the insights the model could provide. Adjusting our PDF, we were able to model different usage types and environments. We separated several zones of the PDF parameter to categorize these types more efficiently.

Analyzing our model's stability through phase portrait analysis and various Jacobian and confusion tests, we developed a better understanding of how our model. Conducting our sensitivity analysis through micro-perturbations and specialized Monte Carlo simulations also increased our confidence in our technique.

Our final steps included using Principal Component Analysis and Bayesian Inference methods to find the most important signals and characteristics of our model and created user recommendations on how to optimize battery life and capacity in the short and long term.

MCM has been an incredible first experience and I'm so glad we were able to participate. We are excited to continue learning and participate again next year!

-Thanks for reading from Bose, Dao and Max.