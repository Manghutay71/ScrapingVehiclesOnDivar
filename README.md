This repository is made for sharing code snippets for scraping vehicles on www.divar.ir (Divar). Divar currently (in 2022) has the most updated car Ads in Iran. So to study the car market and find the best model for real-time prediction of car prices, it's necessary to scrape the car databases on Divar. For better search engine accessibility, Divar provides limited valuable information in the "application/ld+json" script in each HTML webpage. Divar only shows 23 results in this section.

![image](https://user-images.githubusercontent.com/42579060/194767169-2c64c08b-d6f7-4c95-8c37-a2e4c6d233dd.png)

below image shows the content inside "application/ld+json" script.
![divar_1](https://user-images.githubusercontent.com/42579060/194767491-2f08940c-3dad-4cee-9045-1cf39556e968.jpg)

So to use the available information in the "application/ld+json" script instead of scraping every URL of every ad one by one, in the first stage, all the available Car models are classified into two main classes, 1- less Popular and 2- Popular Cars. Popular cars are those that, even in megacities like Tehran, there are less than 23 advertised cars. And vice versa, popular Cars have more than 23 advertisements in some cities.

less popular and popular cars list are available in information.xlsx file.

![information](https://user-images.githubusercontent.com/42579060/194779358-0af8cbe7-c829-4d2d-90ef-ce112196d141.jpg)
