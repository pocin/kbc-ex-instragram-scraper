# About
## configuration

No config.json, the behavior is determined by present tables.

Table `/data/in/tables/user_metadata_from_posts.csv` is present, it must contain one column `post_url`. Other columns are ignored.
This extractor will fetch the post, and extract `user_handle`, `user_name`, `profile_pic_url` from the webpage [1] and save it to  `/data/out/tables/user_metadata_from_posts.csv`. Both tables can be joind on `post_url` column


[1] at this moment it looks for `js` variable `window._sharedData`, serializes this string into JSON and gets the data from there.
Let's see how soon this will break.

## limitations
When post is private/deleted (404 HTTP status code) `None` values are returned for the post
I dont know how the api reacts to scraping, yet so all other 4xx, 5xx codes an exception is raised 
