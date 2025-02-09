## Team
Brandon Kantorski, Jay Roy, Christian Hirschey, and Gavin Ward
## Inspiration
It can be incredibly challenging to navigate life with a health condition or to support those who are facing health challenges. All of us have helped to take care of those with serious health conditions, including early-onset dementia, and have realized how beneficial it could be to have an automated service reminding our loved ones to eat or take their medication since it's unfeasible to care for them 24/7. Due to the difficulties associated with caring for those with serious health challenges, we created MedMonitor to mitigate some of these difficulties and improve the quality of life of those afflicted.
## What it does
Our web app uses a conversational voice AI agent to collect patient data related to medication usage, nutrition, and exercise, giving doctors a centralized monitoring platform to extract relevant insights for medical recommendations, including nutritional intake, exercise, and medication usage. Our services are highly customizable, including the ability to schedule calls for patients of interest ahead of time.
## How we built it
We utilized Retell.ai to extract transcripts from phone calls, and used a pre-trained NLP model to extract nutrition information such as micronutrients and macronutrients from a patient's described meals, as well as calories burned from exercise descriptions. We stored this data in Pinata, utilizing an upgradable smart contract model with a group under each user and custom query handling using py-sdk. Pinata was essential to the security of our application, since client medical data is extremely sensitive and must be handled with care.
## Challenges we ran into
Due to large amounts of requests back and forth between the database we created, Pinata rate-limited us several times, making testing and debugging that much more complex due to how integral Pinata was for our infrastructure.
## Accomplishments that we're proud of
We spent a lot of time working with Pinata to ensure that our data was secure and being handled seamlessly, resulting in a polished final product.
## What we learned
It takes some time to get a fully working database for a complex use case such as this out of Pinata, so it is essential to dive into database design before focusing too heavily on frontend or AI agents.
## What's next for MedMonitor
As more data becomes available for our product, higher quality insights can be derived, particularly relating to nutrition and exercise. We also plan on adding gamification to further motivate patients to achieve their health and wellness goals. 

## Tools Used
OpenAI, Pinata, NextJS, Python, Nutritionix API, FastAPI, Tailwind CSS, Auth0
