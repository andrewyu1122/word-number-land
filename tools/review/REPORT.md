# 素材體檢報告（tools/review_sheets.py，474 個 idle、411 段動畫、227 張 sleep）

對照表：words_1~6.png（36 格/張）、letters.png、numbers.png、dino.png、sea.png、objects.png、garden.png、bosses.png（含 mascot）、scenes.png。
數據在 metrics.json：`fill` = 160px 格子裡不透明像素比例；`sleep_diff` = idle 與 sleep 的平均 RGB 差（0~1）；`anim_diff` = 第 1 格與第 4/7/10/13 格差異的最大值（0~1）。

## a) 風格不一致（寫實 / 太暗 / 沒有臉 / 鏡頭角度不同）
Sketchfab 匯入的模型，貼圖寫實、色調偏暗、臉很小或沒有臉，和自製的圓滾滾卡通角色放在一起落差大：

| 單字 | 問題 |
|---|---|
| butterfly | 照片貼圖、沒有臉 |
| duck | 照片貼圖、沒有臉 |
| chicken | 寫實貼圖、沒有臉 |
| dragon | 寫實模型、沒有臉、側面 |
| dinosaur | 寫實綠色、沒有臉、偏小 |
| tiger | 寫實貼圖、側面、沒有臉 |
| goat | 寫實貼圖、很小 |
| kangaroo | 寫實貼圖、很小、臉看不見 |
| squirrel | 寫實貼圖、很小 |
| hedgehog | 寫實毛皮貼圖、偏暗 |
| elephant | 深灰、側面、臉極小 |
| koala | 深灰、臉極小 |
| castle | 深褐色、整體太暗、眼睛極小 |
| computer | 深色寫實、臉極小 |
| telephone | 黑色寫實、臉極小 |
| backpack | 深藍、臉極小 |
| broccoli | 深綠、偏暗 |
| cookie | 深褐、偏暗 |
| corn | 寫實、偏暗 |
| basketball / football | 寫實貼圖（臉有但很小） |
| bus | 暗黃、純側面、臉很小 |
| bike | 寫實線條、臉很小 |
| airplane / jet | 寫實玩具感、jet 沒有臉 |
| guitar / trumpet / piano | 寫實樂器，臉很小 |
| tree | 寫實低模，臉很小 |
| turtle(words) | 寫實綠龜，臉小 |
| owl | 貼圖風格與其他不同（但可愛，可保留） |
| eagle | 側向、角度不同 |
| shark(words) | 2D 平面貼圖風格 |
| whale(words) | 貼圖漸層風格，和自製的差很多 |
| cloud | 灰色模糊毛球，不像雲 |
| pumpkin | 寫實深橘，偏暗 |
| ant | 腳是細黑線，風格偏硬 |

字母、數字、恐龍、海洋、幼幼、花園、關主：風格一致，沒有這類問題。
objects/car 與 words/car 不同模型（一個寫實紅車一個卡通），可考慮統一。

## b) 太小或太細（`fill` 最低的 40 個，門檻建議 < 0.12）
| objects/feather | 0.044 |
| objects/pencil | 0.057 |
| objects/kite | 0.069 |
| objects/lollipop | 0.071 |
| objects/crayon | 0.074 |
| words/goat | 0.091 |
| objects/flower | 0.095 |
| objects/icecream | 0.099 |
| words/rabbit | 0.101 |
| dino/narwhal | 0.103 |
| words/elf | 0.106 |
| words/lollipop | 0.106 |
| num/n7 | 0.108 |
| words/pencil | 0.111 |
| objects/medal | 0.112 |
| mascot/mascot | 0.113 |
| words/kangaroo | 0.115 |
| garden/tulip | 0.115 |
| words/parrot | 0.12 |
| objects/teddy | 0.121 |
| num/n0 | 0.123 |
| words/fire | 0.124 |
| dino/lobster | 0.124 |
| objects/chick | 0.125 |
| garden/daisy | 0.126 |
| words/candy | 0.127 |
| words/chicken | 0.128 |
| words/emu | 0.128 |
| words/umbrella | 0.128 |
| objects/balloon | 0.128 |
| words/kite | 0.133 |
| dino/manta | 0.134 |
| words/toy | 0.135 |
| objects/pinecone | 0.135 |
| words/tomato | 0.136 |
| num/n5 | 0.138 |
| words/fox | 0.139 |
| dino/seahorse | 0.139 |
| words/squirrel | 0.14 |
| dino/crab | 0.14 |

其中真正需要放大的（在格子裡只佔一小塊，不是本來就細長的物件）：goat、rabbit、elf、kangaroo、parrot、cat、fox、squirrel、toy、tomato、dinosaur、bull、ape、cow、koala、chicken、hen、emu、seahorse、narwhal、mascot。
本來就細長、放大也沒用的：feather、pencil、crayon、lollipop、candy、kite、medal、icecream、flower、n7、n0、n5、tulip、daisy。

## c) 辨識度差（看不出是什麼）
| 單字 | 問題 |
|---|---|
| box | 只是一個棕色立方體加臉 |
| cloud | 灰色毛球，看起來像灰塵 |
| foot | 肉色長條加幾顆球 |
| ham | 粉紅大球加一根白棒 |
| bow | 兩顆粉紅球加兩條，不像蝴蝶結 |
| hamster | 橘色一坨，像馬鈴薯 |
| nose | 粉紅葫蘆形，需要靠上下文 |
| donut | 太扁、顏色太淡，像餅 |
| nut | 深褐大球（像栗子但很暗） |
| giraffe | 方塊拼的，像長頸鹿玩具但頭太小 |
| moth | 淡褐色，翅膀花紋不明顯 |
| mountain | 灰色圓丘，不像山 |
| jet | 灰色塊狀飛機、沒有臉 |
| wave | 藍色斜塊，要靠泡泡才看得出 |
| web | 灰色輪子狀，像車輪 |
| road | 灰板子加路標 |
| log | 還可以，但端面年輪太淡 |
| saw | 還可以 |
| rat / mouse | 兩個很像，mouse 深灰 rat 淺灰 |
| objects/acorn | 灰色多面體，不像橡實 |
| objects/pretzel | 褐色圓片，不像蝴蝶餅 |
| objects/shell | 米色一坨 |
| objects/seashell | 粉紅扇形，勉強 |
| garden/snail | 黃色大球加灰色小蝸牛，比例怪 |
| garden/peacock | 藍綠色一塊，看不出孔雀 |
| garden/hedgehog | 棕色一坨加刺 |

## d) sleep 和 idle 幾乎一樣（`sleep_diff` 最低的 30 個）
| num/n20 | 0.0127 |
| num/n18 | 0.0142 |
| num/n15 | 0.0169 |
| num/n13 | 0.0175 |
| num/n16 | 0.018 |
| num/n17 | 0.0183 |
| num/n12 | 0.0191 |
| num/n11 | 0.022 |
| num/n19 | 0.0224 |
| num/n14 | 0.0269 |
| words/elephant | 0.0471 |
| words/pumpkin | 0.0586 |
| words/nut | 0.0604 |
| words/koala | 0.0611 |
| words/castle | 0.0645 |
| words/volcano | 0.067 |
| words/backpack | 0.0674 |
| words/butterfly | 0.0682 |
| words/house | 0.0705 |
| words/telephone | 0.072 |
| words/mountain | 0.0733 |
| words/apple | 0.0747 |
| words/ape | 0.0762 |
| words/broccoli | 0.0765 |
| words/corn | 0.0772 |
| words/coin | 0.0777 |
| words/monkey | 0.078 |
| words/lobster | 0.0781 |
| words/tent | 0.0781 |
| words/cookie | 0.0783 |

- n11~n20：sleep 只閉眼，身體沒變化（數字角色原本就沒設計趴下），差異 0.01~0.03。
- Sketchfab 匯入的字（elephant、koala、castle、backpack、butterfly、volcano、house、mountain、telephone、octopus、ape、monkey、bear、chicken、lobster…）沒有可控的眼睛，sleep 只有縮小 7% 和低頭 6 度，幾乎看不出在睡。
- 自製角色的 sleep 有眼皮，差異普遍 0.1 以上，算正常。

## e) 動畫幅度最小的 45 個（`anim_diff`，中位數 0.255）
| words/rat_anim | 0.0215 |
| mascot/mascot_wave | 0.0301 |
| words/taxi_anim | 0.0331 |
| words/camel_anim | 0.0367 |
| words/donut_anim | 0.0374 |
| words/train_anim | 0.0381 |
| words/pin_anim | 0.0384 |
| words/truck_anim | 0.0384 |
| words/whale_anim | 0.0417 |
| words/bus_anim | 0.0427 |
| mascot/mascot_xmas_wave | 0.0429 |
| dino/ankylosaurus_walk | 0.0447 |
| words/athlete_anim | 0.0449 |
| words/crocodile_anim | 0.0449 |
| words/pony_anim | 0.0451 |
| words/turtle_anim | 0.0455 |
| garden/bunny_move | 0.0466 |
| words/ambulance_anim | 0.0483 |
| words/octopus_anim | 0.0483 |
| words/snake_anim | 0.0489 |
| words/horse_anim | 0.0491 |
| words/gem_anim | 0.0499 |
| words/car_anim | 0.0502 |
| words/van_anim | 0.0527 |
| dino/brachiosaurus_walk | 0.0538 |
| words/pumpkin_anim | 0.0551 |
| words/crab_anim | 0.0555 |
| words/hedgehog_anim | 0.0556 |
| garden/turtle_move | 0.058 |
| dino/stegosaurus_walk | 0.0587 |
| words/duck_anim | 0.0589 |
| words/tornado_anim | 0.0595 |
| garden/snail_move | 0.0597 |
| words/lobster_anim | 0.06 |
| words/tractor_anim | 0.061 |
| dino/diplodocus_walk | 0.0612 |
| words/seal_anim | 0.0618 |
| words/road_anim | 0.0624 |
| words/cookie_anim | 0.0643 |
| dino/spinosaurus_walk | 0.0655 |
| words/pencil_anim | 0.0677 |
| words/ghost_anim | 0.0699 |
| dino/trex_walk | 0.0738 |
| words/bike_anim | 0.0762 |
| words/ant_anim | 0.0769 |

- drive 類（bus taxi truck train van car tractor ambulance pony horse camel road）：只有 4 公分上下彈動和輪子轉，最弱。
- 恐龍 walk（ankylosaurus brachiosaurus stegosaurus diplodocus spinosaurus trex…）：腳擺 24 度但身體幾乎不動，看起來很靜。
- mascot_wave / mascot_xmas_wave：只有一隻手揮，幅度小。
- wiggle 類（rat donut pin gem pumpkin crab hedgehog duck lobster cookie pencil…）：±12 度搖擺偏小。
- 花園 move（bunny turtle snail）：只是平移抖動。

## 數字 idle 腳底不一致（任務 3 相關）
numbers.png 可以看到 n11~n19 的腳底比 n21~n100 高，n0/nq 又不同；n100 比 n90 小。alpha bbox 底邊各不相同，需要統一。
