Inside PostgreSQL:

Total Sales:
SELECT SUM(Price_usd)
FROM fashion_resale
WHERE Sold = TRUE

2599660

Total items Sold:
SELECT COUNT(Sold)
FROM fashion_resale
WHERE Sold = TRUE

11941

 Avg price
 SELECT
COUNT(Sold) as item_amount,
SUM(Price_usd) as total_sold,
    SUM(Price_usd) / COUNT(Sold) AS avg_price_per_item
FROM fashion_resale

331.54

    - How many items sold in precentage from total items listed
 <<<SQL does not count Bool values>>>
SELECT
	SUM(CASE WHEN Sold = True THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as Sold_precentage
FROM fashion_resale;

1.53%

    - Revenue by category

    SELECT Product_category,
	ROUND(SUM(Price_usd)) AS category_revenue
FROM fashion_resale
WHERE Sold = True
GROUP by Product_category


"product_category"	"category_revenue"
"Men Accessories"	      176851
"Men Clothing"	          509027
"Men Shoes"	              334374
"Other"	                    964
"Women Accessories"       99562
"Women Clothing"	      711402
"Women Shoes"	          767480

    - Revenue by season

SELECT Product_season,
	ROUND(SUM(Price_usd)) AS category_revenue
FROM fashion_resale
WHERE Sold = True
GROUP by Product_season


"product_season"	"category_revenue"
"All seasons"	        2160206
"Autumn / Winter"   	255583
"Spring / Summer"	    183872

--------------------------------------------------------------------------------------

2. Seller performance
    - Total per seller TOP 10
SELECT Seller_id,
ROUND(SUM(CASE WHEN sold THEN seller_earning ELSE 0 END)) AS total_earning
From fashion_resale
GROUP BY  Seller_id
ORDER BY total_earning DESC
LIMIT 10

Earnings FROM DATASET
"seller_id"	"total_earning"
48600	        15131
12698884	    11907
16059674	    9063
1161554	        8742
9071862	        7801
19230235	    5952
1760381	        5382
16886144	    5238
15886961	    4992
6633364	        4412


SELECT Seller_id,
ROUND(SUM(Seller_earning)) as total_earning
From fashion_resale
GROUP BY  Seller_id
ORDER BY total_earning DESC
LIMIT 10

Earnings THROUGHOUT HISTORY
seller_id   total_earning
13276748	   5971806
4153869	       3621529
6633364	       2151672
8580538	       1455323
16774308	   1411365
22899198	   1399727
19227665	   1122239
13364481	   997200
16465877	   989631
11080210	   897212




    - Total items sold per seller TOP 10

Had to use MAX as seller_products_sold vary a bit.
That column shows total items sold SUM is not an option.

SELECT Seller_id,
       SUM(CASE WHEN sold THEN 1 ELSE 0 END) AS total_sold
FROM fashion_resale
GROUP BY Seller_id
ORDER BY total_sold DESC
LIMIT 10;


SOLD FROM DATASET
"seller_id"	"total_sold"
9071862	        64
48600	        50
12698884	    48
15397859	    45
9360167     	41
18325692	    40
3404357	        29
18136264	    20
15622481	    18
15886961	    18

SOLD THROUGHOUT HISTORY
SELECT Seller_id,
       MAX(seller_products_sold) AS total_sold
FROM fashion_resale
GROUP BY Seller_id
ORDER BY total_sold DESC
LIMIT 10;

"seller_id"	"total_sold"
48600	        79738
9071862	        38592
6508493	        23235
12698884	    22552
10056903	    15551
9360167	        13892
3404357	        13148
1760381	        11795
4085582	        11140
1161554	        10812


    - Avg earing per sold item

SELECT
    Seller_id,
    ROUND(SUM(CASE WHEN sold THEN seller_earning ELSE 0 END)) AS total_earning,
    SUM(CASE WHEN sold THEN 1 ELSE 0 END) AS total_sold,
    ROUND((SUM(CASE WHEN sold THEN seller_earning ELSE 0 END) * 1.0 /
        NULLIF(SUM(CASE WHEN sold THEN 1 ELSE 0 END), 0))) AS avg_earning_per_item
FROM fashion_resale
GROUP BY Seller_id
HAVING SUM(CASE WHEN sold THEN 1 ELSE 0 END) > 0
ORDER BY total_sold DESC
LIMIT 10;


"seller_id"	"total_earning"	"total_sold"	"avg_earning_per_item"
9071862     	7801	        64	                122
48600	        15131	        50	                303
12698884	    11907	        48	                248
15397859	    2550	        45	                57
9360167	        3463	        41	                84
18325692	    4246	        40	                106
3404357	        3981	        29	                137
18136264	    4100	        20	                205
15622481	    3957	        18	                220
15886961	    4992	        18	                277



- Top seller countries

SELECT Seller_country, COUNT(*) as amount
FROM fashion_resale
GROUP BY Seller_country
ORDER BY amount DESC
LIMIT 10;

"seller_country"	"amount"
"Italy"	            205419
"France"	        112162
"United States"	    105325
"United Kingdom"	66583
"Germany"	        38098
"Spain"	            37681
"Poland"	        26654
"Japan"	            18075
"Romania"	        17124
"Greece"	        13088

--------------------------------------------------------------------------------------------