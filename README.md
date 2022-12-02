# new_world_music_bot
Bot for afk playing music and get music xp

--------------------------------------------------------------------------------------------------
## How to run
### 1. Install python 3.10
You can get python 3.10 [here](https://www.python.org/downloads/release/python-3100/)

### 2. Create venv with requirements
#### 2.1 Create env
```shell
python3 -m venv venv
```
#### 2.2 Activate env
```shell
./venv/scripts/activate.ps1
```
#### 2.3 Install requirements
```shell
pip install -r requirements.txt
```

### 3. Run bot
```shell
python3 new_world_music_bot.py
```

--------------------------------------------------------------------------------------------------
## Config explanation
There is [configuration file](/Resource/config.ini) in Resource dir

You can customize some settings there

### GLOBAL section
<table>
    <tr>
        <th>Variable</th>
        <th>Type</th>
        <th>Default value</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>max_songs</td>
        <td>int</td>
        <td>10</td>
        <td>Quantity of songs to play. You can choose between 0 and 10000. 0 means play until stopped.</td>
    </tr>
</table>

### TIMINGS section
<table>
    <tr>
        <th>Variable</th>
        <th>Type</th>
        <th>Default value</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>mouse_press</td>
        <td><code>int</code> <code>float</code></td>
        <td>0.15</td>
        <td>The time the button is pressed for in song (left + right mouse buttons) in seconds</td>
    </tr>
    <tr>
        <td>performance_end</td>
        <td><code>int</code> <code>float</code></td>
        <td>7</td>
        <td>How long to wait before finishing the performance in seconds</td>
    </tr>
    <tr>
        <td>between_songs</td>
        <td><code>int</code> <code>float</code></td>
        <td>1</td>
        <td>Time to wait between songs in seconds</td>
    </tr>
    <tr>
        <td>screenshot_frequency</td>
        <td><code>int</code> <code>float</code></td>
        <td>0.05</td>
        <td>Main cycle frequency in seconds</td>
    </tr>
    <tr>
        <td>before_start</td>
        <td><code>int</code></td>
        <td>5</td>
        <td>Time to wait before start in seconds</td>
    </tr>
</table>

### SCREENSHOT section
<table>
    <tr>
        <th>Variable</th>
        <th>Type</th>
        <th>Default value</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>x_offset</td>
        <td><code>int</code></td>
        <td>10</td>
        <td>Screenshot x offset (to the right)</td>
    </tr>
    <tr>
        <td>box_x_0</td>
        <td><code>int</code></td>
        <td>815</td>
        <td>Screenshot box coordinate (left upper corner)</td>
    </tr>
    <tr>
        <td>box_x_1</td>
        <td><code>int</code></td>
        <td>817</td>
        <td>Screenshot box coordinate (right lower corner)</td>
    </tr>
    <tr>
        <td>box_y_0</td>
        <td><code>int</code></td>
        <td>1050</td>
        <td>Screenshot box coordinate (left upper corner)</td>
    </tr>
    <tr>
        <td>box_y_1</td>
        <td><code>int</code></td>
        <td>1250</td>
        <td>Screenshot box coordinate (right lower corner)</td>
    </tr>
</table>

### SONGS sections
`SONGS` sections represent in-game music sheets

Sheets divided by 3 levels: `SONGS NOVICE`, `SONGS SKILLED` and `SONGS EXPERT` sections

Music sheet consists of 6 "notes": `w`, `a`, `s`, `d`, `#` (mouse buttons), `_` (space)

You can add any custom sheets for yourself by just adding variable to one of sections
with any name
