# makefun-news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Keso1234/makefun-news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Keso1234/makefun-news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A dense broadsheet newspaper front page summing up the world's news of Tuesday 24 November 2026. The whole page is drawn by `main.py` using only the Python standard library — no network, no third-party packages, no external files.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 -P -s main.py
```

Writes `out/entry.png` (1024x1024, under 1 MiB). The program is fully deterministic: two runs write byte-identical files.

## What is on the page

- Masthead plus a markets ticker (Tuesday's closes: Dow +0.9%, S&P 500 -0.5%, Nasdaq -1.5%, Nvidia -5.9%, Nikkei +3.9%, gold $3,550, bitcoin $59,500, WTI $81.45).
- Lead story: the US is ready to slap tariffs on China, the EU and 14 other economies over subsidised production. Two secondaries: the Shenzhou-24 crew unveiled at Jiuquan, with a Pakistani astronaut set to fly, and fourteen nations backing the ICJ's Rohingya ruling.
- A colour world map with eight numbered story locations.
- A timeline of the day with the times each event was reported.
- Twenty more stories in four columns (conflict, world, politics, business and sport), each carrying its source.
- Twelve more stories in brief.
- A red date-check box: Tuesday 24 November 2026.

Every story states only what reports published on 24 November 2026 said. Sources: AP, Reuters, BBC, Dow Jones, UN News, ISW, ESA.

<sub>Entered on [make.fun](https://make.fun/?ref=taaana65&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
