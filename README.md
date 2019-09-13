# FLAAS
Facebook Link - As A Service

Pass OpenGraph metadata via GET parameters
Can be used on Facebook, Reddit, or any site that uses OpenGraph for link metadata

Example - http://heraldoftherepublic.ga/News/Anime/EN/1235234sasd2/Araki-Sensei-Confirms-Part-6-Adaption-For-Spring-2020/?i=https://i.imgur.com/3UvF08p.jpg

How it looks on Reddit - https://www.reddit.com/r/ShitPostCrusaders/comments/d14782/araki_confirms_part_6_stone_ocean_adaption_for/

Link Settings
  i = Thumbnail image
  t = Title
  d = Description
  u = URL (currently hardcoded as "")
  p = Post type (currently hardcoded as "Article")

Setting up
  Rename config_example.json to config.json with server settings
  Run main.py in Python3
