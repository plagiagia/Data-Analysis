## Project description
For this project, we take the role of a data analyst and investigate the data of an online ticket store. We are provided we three tables, one with the visits data, the orders, and the costs of marketing expenses. 

## Conclusion
We finally went through all the important metrics and analyzed how revenue, costs, and customer metrics change in comparison with other features such as cohort, different devices, or ad sources.
More specific we saw that our services depend on new users. We calculated that 84% of the weekly visitors are new users, and only 4% of the monthly visitors are returned, customers.
Next, we calculated the average time spent on our site for a session. This metric is skewed and unbalanced. To take the mean from such a feature is not representative of the whole population. That's why we choose the mode/most frequent value and that is 60 seconds.
So till now, we know that our services attract new customers more than the old ones and they tend to spend around 60 seconds on our site.
To find out where the problem is and when we lose our old customers we calculated the retention matrix. This matrix showed us the rate that a registered user will come back a specific month after his first registration. The result helps us to prove that the monthly retention was 4%. In some cases, we notice a minor increase but only due to seasonality. Furthermore, we calculated the retention compared with the device a user uses, and there is a slight difference between desktop users and touch screen users, with the first ones being more loyal than the latter.
Going further we wanted to calculate when a user is converted to a buyer. The results showed that a user converted to buyers:
- 75% of the time the first two days
- 25% of the time in weeks or months

So this can explain the fact why retention is so small as users converted to customers most of the time the first day of their visit and after that, they don't come back so frequently for a purchase. To see if we have sound results we calculated the conversion rate for different features such as the device or the source. This showed us that:
- Desktop users converted the same day
- Touch users after the first day
- There ad sourced that need some optimization

Dividing customers into buckets depending on their conversion time we draw some useful conclusions.
- Quick buyers bring the money to the company due to their quantity as they tend to buy on average cheap but many.
- Week buyers follow in quantity but they spend even less than the quick buyers on a purchase.
- Three-month buyers were the most important ones as they tend to spend more on purchases on average but not so many products.
- Other categories are not so important.

Analyzing the orders we found out that on average each day 140 orders were placed with this number to increase when holidays arrive.
The average price of each order is 5 dollars with this number to reach 30 when the holidays arrive.
Next, we want to find out how much value each customer has. Calculating the LTV we saw a customer loses his value after his first purchase. But interesting enough we see that after three months we see a slight increase. This proves the fact that Three Month buyers from the previous analysis bring some value to the company.

**What do we know till now?**

- The company depends on new users
- A user tends to be converted to a customer the first day of the visit
- These users or else the quick buyers bring revenue because of the number of their purchases. They buy cheap.
- There is an interesting behavior for the three months buyers category.
- Customer Life Time Value for each cohort drops after the first month of life.
Now that we know how revenue is created and how customers behave we can analyze the costs and marketing expenses so we know if we are profitable.
- For the year the data were collected we spent 330000\$
- On average we spent 27427\$ each month
- The most expensive ad source was this with id 3

Customers come through some sources to our site, for each source we spent an amount of money. Each time to see much money costs the acquisition of a customer for a specific source.
- The most expensive source was the 3 and seems not to be the most effective concerning the number of customers it brings.
- The source with id 4 was in the top three most expensive but in a matter of CAC have one of the lowest values. It is working as it should.
- Lastly, we calculated the relation of the costs for each month with the revenue. The results showed that the company didn't break even in any of the months. It spends more than it makes.


**Recommendations**

As our services are to sell tickets to users it makes sense that most of the time a visitor converted to a buyer at the same time of the visit. The thing is that these users are not loyal enough to come back to us when they need again a ticket. It seems that they use us after a search on the web for a specific event. We have to make a campaign so that a registered user next time that wants to buy a ticket will visit direct our site for purchase. We saw this behavior for the Three-Month buyers. They probably registered and then waited for a specific event three months, maybe a concert or something like that. Tickets for these events are expensive and users tend to scout the best deals months before they buy. It seems that these users are the most profitable and maybe we can attract more of them by offering early-bird offers. Also, we need to optimize our ad sources as we spend more to acquire a customer than what he pays in his life as a registered user on our site. Maybe offering a discount to users when they bring a friend will work better, as they will be more loyal and also they will do the job of an ad.
