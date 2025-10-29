# 📺 DASH/MPD Support Guide

## ✅ **DASH/MPD is Fully Supported!**

IBE-100 v2.0.3 supports **DASH (Dynamic Adaptive Streaming over HTTP)** with **MPD (Media Presentation Description)** manifest files.

---

## 🎯 **What is DASH/MPD?**

- **DASH** = Dynamic Adaptive Streaming over HTTP (ISO/IEC 23009-1 standard)
- **MPD** = Media Presentation Description (manifest file - like `.m3u8` for HLS)
- **Segments** = `.m4s` or `.ts` media files
- **Standard:** MPEG-DASH (used by YouTube, Netflix, etc.)

---

## 🚀 **How to Use DASH Output**

### **Step 1: Configure DASH**

1. **Stream Configuration Tab:**
   - **Output Type:** Select `DASH`
   - **DASH Output Directory:** `output/dash` (or your path)
   - **Segment Duration:** 6 seconds
   - **Playlist Window:** 5 segments
   - **Enable CORS:** ✅ (important for web players)

### **Step 2: Start Stream**

1. Configure input stream
2. Generate SCTE-35 marker (optional)
3. Click **"Start Stream"**

### **Step 3: Files Generated**

In `output/dash` directory:
```
output/dash/
  ├── stream.mpd          ← Main MPD manifest file
  ├── stream-000000.m4s   ← Media segments
  ├── stream-000001.m4s
  └── stream-000002.m4s
  ...
```

---

## 🌐 **Serving DASH with Web Server**

### **Using Built-in Web Server:**

1. **Start Web Server:**
   - Go to **Monitoring → Web Server** tab
   - **Port:** 8000
   - **Serving Directory:** `output/dash` ← Must match DASH output directory!
   - Click **"Start Web Server"**

2. **Access MPD File:**
   ```
   http://localhost:8000/stream.mpd
   ```

### **Important Notes:**

- ✅ Web server auto-creates directory if missing
- ✅ CORS headers automatically added
- ✅ Works exactly like HLS web server
- ✅ Both HLS and DASH can be served from same server (different directories)

---

## 🎬 **Playing DASH Streams**

### **Option 1: Test Player (Included)**

1. Open `test_player.html` in browser
2. **URL:** `http://localhost:8000/stream.mpd`
3. **Type:** Select "DASH"
4. Click **"Load Stream"** then **"Play"**

### **Option 2: Dash.js Player**

```html
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/dashjs@latest/dist/dash.all.min.js"></script>
</head>
<body>
    <video id="videoPlayer" controls width="800"></video>
    <script>
        const url = "http://localhost:8000/stream.mpd";
        const player = dashjs.MediaPlayer().create();
        player.initialize(document.querySelector("#videoPlayer"), url, true);
    </script>
</body>
</html>
```

### **Option 3: Shaka Player**

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/shaka-player/4.7.0/shaka-player.compiled.js"></script>
<script>
    const video = document.getElementById('video');
    const player = new shaka.Player(video);
    player.load('http://localhost:8000/stream.mpd');
</script>
```

---

## 📋 **DASH vs HLS**

| Feature | HLS | DASH |
|---------|-----|------|
| **Manifest** | `.m3u8` | `.mpd` |
| **Segments** | `.ts` | `.m4s` or `.ts` |
| **Standard** | Apple HLS | MPEG-DASH (ISO) |
| **Browser** | Safari native | Chrome/Firefox native |
| **Mobile** | iOS native | Android native |
| **Player** | HLS.js, Video.js | Dash.js, Shaka Player |

---

## 🔧 **TSDuck DASH Command**

Your app generates:

```bash
tsp -I hls https://input.m3u8 \
    -P spliceinject --files marker.xml \
    -O hls --live output/dash \
           --dash \
           --segment-duration 6 \
           --playlist-window 5 \
           --cors *
```

**Key:** `-O hls --dash` generates `.mpd` instead of `.m3u8`

---

## ✅ **Complete DASH Workflow**

1. ✅ **Configure:** Output Type = DASH
2. ✅ **Set Directory:** `output/dash`
3. ✅ **Enable CORS:** Check checkbox
4. ✅ **Start Stream:** Generate DASH output
5. ✅ **Start Web Server:** Serve `output/dash` directory
6. ✅ **Play:** Use `http://localhost:8000/stream.mpd`

---

## 🎯 **Web Server Directory Setup**

**Important:** Web server directory must match DASH output directory!

```
If DASH Output Directory = "output/dash"
Then Web Server Directory = "output/dash"
Then Access URL = "http://localhost:8000/stream.mpd"
```

---

## 📝 **Troubleshooting**

### **MPD file not found?**
- Check output directory path
- Verify stream has started processing
- Make sure web server directory matches output directory

### **CORS errors?**
- Enable CORS checkbox in app
- Web server adds CORS headers automatically

### **Player not working?**
- Verify MPD file exists: Open `http://localhost:8000/stream.mpd` in browser
- Check segment files exist in same directory
- Verify web server is running

---

**DASH/MPD is fully functional! Use it just like HLS.** 🎉

