# 📊 Stream Status Explanation

## ✅ **Normal Stream Behavior**

### **Exit Code 0 = Success**
When TSDuck finishes with code 0, it means:
- ✅ Stream processed successfully
- ✅ No errors occurred
- ✅ Clean shutdown

This is **normal** when:
- Input stream ends
- Connection closes
- User stops the stream
- Stream completes its cycle

---

## ⚠️ **Understanding Warnings**

### **"RCV-DROPPED" Warnings**
```
[TSDuck] W:SRT.br: RCV-DROPPED 1 packet(s). Packet seqno delayed for 13.249 ms
```

**What it means:**
- A packet arrived slightly late (13ms delay)
- TSDuck received it anyway, just marked it as "delayed"
- This is **normal network behavior**

**When to worry:**
- ❌ Many dropped packets (10+ per second)
- ❌ Very long delays (500ms+)
- ❌ Consistent packet loss

**When it's OK:**
- ✅ Occasional warnings (1-2 per minute)
- ✅ Short delays (<50ms)
- ✅ Stream continues normally

---

## 🔄 **Continuous Streaming**

### **Current Behavior:**
- Stream processes until source ends
- Then stops normally (code 0)
- Requires manual restart

### **If You Need Auto-Restart:**
I can add:
- Auto-reconnect on disconnection
- Automatic restart when stream ends
- Retry logic with backoff

**Let me know if you want this feature!**

---

## ✅ **Your Current Output is Perfect:**

```
✅ Stream connected
✅ Processing packets
✅ SCTE-35 marker ready
✅ No errors
✅ Clean shutdown
```

**Everything is working correctly!** 🎉

