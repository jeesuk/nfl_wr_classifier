# nfl_wr_classifier
A model that categorizes NFL wide receivers by playing style, using the following data:
- Play-by-play data from Sportradar (via API)
- Receiver-level data from Pro Football Focus Premium
- Receiver-level data from the NFL Scouting Combine (via nflverse library)
  - Physical attributes and metrics in the Combine drills often indicate how the receiver is best used
- Receiver-level data from NFL Next Gen Stats (via nflverse library)
  - Uses RFID to track player movements

## Notes
- Currently covers receivers from the 2022 regular season.
- I created new features to account for specific situations that call on certain styles of receivers.
  - For example, a "possession receiver" would be ideal for a pass play in which 7 yards are needed for a first down conversion and the quarterback throws the ball 7 air yards.
- One game from the 2022 regular season is ommitted - the week 17 BUF-CIN game in which Damar Hamlin suffered cardiac arrest and was subsequently canceled.

## Future Changes
- I need to scale the features and do something to reduce the number of features. I'll probably use PCA.
- I'll likely use K-Means clustering to categorize receivers.
- Will eventually include different seasons so that a unique player-season pair represents one row.
