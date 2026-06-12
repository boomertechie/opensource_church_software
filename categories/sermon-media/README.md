# Sermon Media & Podcast Hosting
*Self-hosted sermon distribution, podcast management, and media archives*

> **What it is:** Software for hosting, distributing, and managing sermon audio/video content, podcast feeds, and media libraries.

## Why It Matters

- **Sermon archives** are permanent ministry assets that should outlive any third-party platform
- **Podcast distribution** requires RSS feeds that major platforms (Apple, Spotify) can consume
- **Self-hosting** ensures your sermons remain accessible even if hosting services shut down or change policies
- **Transcription** makes sermons searchable and accessible to deaf/hard-of-hearing members
- **Analytics** help understand which content resonates and reaches your congregation
- **Cost control** matters when your archive grows to hundreds or thousands of sermons
- **Federation** allows church networks to share content without centralized control

---

## Castopod

**Status:** Active (December 2025) | **Skill Level:** Intermediate | **License:** AGPL-3.0

**True Cost:** $5-15/month hosting + domain; free software

### What It Does

Full-featured podcast hosting platform designed for self-hosting. Creates RSS feeds compatible with Apple Podcasts, Spotify, Google Podcasts, and other directories. Built-in analytics dashboard, video clip creation tools, and social media promotion features. Podcasting 2.0 certified with support for chapters, transcripts, and location data.

### Why Churches Use It

Churches choose Castopod when they want professional podcast distribution without ongoing per-episode costs. The Fediverse integration means sermons can reach people through Mastodon and other ActivityPub platforms. IABv2-compliant analytics provide genuine listener data without privacy concerns. The platform handles the technical complexity of podcast RSS while maintaining full data ownership.

### Installation

Docker deployment recommended. Requires PHP 8.1+, MySQL/MariaDB, and web server (Apache/Nginx). Official Docker Compose configuration simplifies setup. Storage needs scale with sermon archive size (plan ~100MB per hour of audio). CDN integration available for larger churches.

### Caveats

More complex than simply uploading to YouTube. Requires understanding of RSS feeds and podcast directory submission. Initial setup takes 2-4 hours for someone comfortable with Docker. Video features require ffmpeg and adequate server resources. Best suited for churches committed to maintaining their own infrastructure.

### Links

- Website: https://castopod.org
- GitHub: https://github.com/ad-aures/castopod
- Documentation: https://docs.castopod.org

---

## Podcast Generator

**Status:** ⛔ Not Recommended — Repository archived April 2026

The upstream repository was archived on 2026-04-04 with no successor named. **Use Castopod above** — it's maintained, more capable, and the right choice for new deployments. Existing Podcast Generator installs will keep running, but don't start a new one.

- Original repo (for reference): https://github.com/PodcastGenerator/PodcastGenerator

---

## PeerTube

**Status:** Very Active | **Skill Level:** Advanced | **License:** AGPL-3.0

**True Cost:** $15-40/month VPS for small instances; free software

### What It Does

Federated video hosting platform (decentralized YouTube alternative). Supports live streaming, video-on-demand, playlists, and user subscriptions. Federation allows multiple PeerTube instances to share content and viewers. Built-in transcoding, quality levels, and embed capabilities. Supports plugins for extended functionality.

### Why Churches Use It

Churches wanting video sermon archives without YouTube's terms of service or algorithm control. Federation means denominational networks can interconnect instances while maintaining independence. Live streaming capability supports online worship services. Viewer data stays private and server-controlled.

### Installation

Requires Node.js, PostgreSQL, Redis, and Nginx/Apache. Official Docker installation available. Transcoding demands significant CPU/GPU resources. Storage scales with video archive (plan 1-5GB per hour depending on quality). Professional deployment recommended for production use.

### Caveats

Resource-intensive compared to podcast-only solutions. Transcoding can overwhelm small servers. Federation complexity may confuse non-technical users. Best suited for churches with technical expertise or managed hosting. Initial setup 4-8 hours minimum.

### Links

- Website: https://joinpeertube.org
- GitHub: https://github.com/Chocobozzz/PeerTube
- Instance List: https://instances.joinpeertube.org

---

## Navidrome

**Status:** Active | **Skill Level:** Beginner-Intermediate | **License:** GPL-3.0

**True Cost:** $5-15/month hosting or free on home server; free software

### What It Does

Self-hosted music and audio streaming server with Subsonic API compatibility. Supports playlists, favorites, smart playlists, and multi-user access. Mobile apps available through Subsonic ecosystem. Automatic music library scanning and metadata management.

### Why Churches Use It

Excellent for sermon audio archives organized by series, speaker, or topic. Members can stream sermons through mobile apps (dsub, Ultrasonic, play:Sub). Works well for internal staff access to full sermon library. Lightweight resource requirements suit home servers or small VPS.

### Installation

Single binary deployment or Docker container. Requires only file storage for audio files. Automatically scans folder structure and builds library. Setup takes 15-30 minutes. Works on Linux, Windows, macOS, and Raspberry Pi.

### Caveats

Designed for music, not podcasts—no RSS feed generation. Requires members to use Subsonic-compatible apps rather than standard podcast apps. Better as internal sermon archive than public distribution tool. No built-in transcription or video support.

### Links

- Website: https://www.navidrome.org
- GitHub: https://github.com/navidrome/navidrome
- Compatible Apps: https://www.navidrome.org/docs/overview/#apps

---

## Audiobookshelf

**Status:** Very Active | **Skill Level:** Beginner | **License:** GPL-3.0

**True Cost:** Free on home server or $5-15/month VPS; free software

### What It Does

Self-hosted audiobook and podcast server with beautiful interface. Organizes audio content as "books" (perfect for sermon series). Progress tracking, playback speed control, sleep timer, and bookmarking. Mobile apps for iOS and Android. Supports podcasts with automatic download management.

### Why Churches Use It

Natural fit for organizing sermon series as "audiobooks" with chapters for individual messages. Members can track their progress through teaching series. Excellent for churches wanting to present sermons more like courses or studies. User-friendly interface lowers adoption barriers.

### Installation

Docker or binary installation. Requires storage for audio files and small SQLite database. Auto-detects folder structures and organizes content. Setup takes 20-40 minutes. Reverse proxy recommended for external access.

### Caveats

Primarily designed for audiobooks, not traditional podcast distribution. No RSS feed generation for external podcast directories. Better suited for member access than public evangelism. Video support limited. Best as complement to, not replacement for, traditional podcast hosting.

### Links

- Website: https://www.audiobookshelf.org
- GitHub: https://github.com/advplyr/audiobookshelf
- Documentation: https://www.audiobookshelf.org/docs

---

## Whisper (Speech-to-Text)

**Status:** Active | **Skill Level:** Intermediate-Advanced | **License:** MIT

**True Cost:** Free for CPU inference; GPU recommended ($300+ hardware or $0.50-2/hour cloud GPU)

### What It Does

OpenAI's open-source automatic speech recognition system. Transcribes sermon audio to text with high accuracy (90-95% typical). Supports 99 languages. Multiple model sizes from tiny (fast, less accurate) to large (slow, very accurate). Can add punctuation and formatting automatically.

### Why Churches Use It

Makes sermon archives searchable and accessible. Transcripts benefit deaf/hard-of-hearing members and enable translation workflows. Search functionality helps staff find sermon references. Transcripts improve SEO for sermon websites. One-time transcription beats ongoing transcription service costs.

### Installation

Python 3.8+ required. Install via pip. CPU-only version works but processes slowly (1 hour audio = 10-30 minutes processing). GPU dramatically improves speed (1 hour audio = 2-5 minutes with good GPU). Can run on home computer or cloud instances.

### Caveats

Requires technical comfort with Python and command line. GPU acceleration needs NVIDIA CUDA setup. Large models demand significant RAM (10GB+ for best quality). Accuracy varies with audio quality and accents. May require manual editing of output. Not real-time for live services.

### Links

- GitHub: https://github.com/openai/whisper
- Model Card: https://github.com/openai/whisper/blob/main/model-card.md
- Community Guides: https://huggingface.co/openai/whisper-large-v3

---

## ChurchApps Suite (Content Module)

**Status:** Active | **Skill Level:** Beginner-Intermediate | **License:** MIT/GPL-3.0

**True Cost:** Free cloud tier or self-hosted; free software

### What It Does

Integrated church management platform including content/lesson management. Handles sermon notes, small group curriculum, and media attachments. Connects with attendance, giving, and communication modules. Mobile app support for member access.

### Installation

Cloud-hosted free tier available (easiest start). Self-hosted Docker deployment for full control. Requires MySQL/PostgreSQL and Node.js environment. Documentation covers both deployment paths.

### Caveats

Content management is one module of larger church management system—may be overkill if you only need sermon hosting. Less specialized than dedicated podcast platforms. Better suited for churches wanting all-in-one solution. Self-hosting requires maintaining entire stack.

### Links

- Website: https://churchapps.org
- GitHub: https://github.com/ChurchApps
- Demo: https://b1.church

---

## Comparison Matrix

| Platform | Best For | Podcast RSS | Video | Transcription | Complexity | Resources |
|----------|----------|-------------|-------|---------------|------------|-----------|
| **Castopod** | Professional podcast distribution | Yes | Clips only | No | Medium | Medium |
| **PeerTube** | Video sermon archives + live streaming | Limited | Yes | No | High | High |
| **Navidrome** | Internal audio library for staff/members | No | No | No | Low | Very Low |
| **Audiobookshelf** | Sermon series organized as "courses" | No | No | No | Very Low | Low |
| **Whisper** | Adding transcripts to existing content | N/A | N/A | Yes | Medium-High | High (GPU) |
| **ChurchApps** | All-in-one church management | Limited | Yes | No | Medium | Medium |

---

## Recommendations by Church Size

### Small Churches (Under 100)

**Start Here:** Castopod

- **Castopod** is the right baseline — maintained, professional, full RSS + analytics
- If Docker feels like too much, the simplest path is to host audio on Nextcloud or a static site and hand-write the podcast RSS feed (a single XML file the church website serves)
- **Consider:** Audiobookshelf for organizing sermon series for internal member access
- **Skip:** PeerTube (too resource-intensive unless video is primary format)

### Medium Churches (100-500)

**Start Here:** Castopod

- **Castopod** provides professional podcast distribution at this scale
- **Add:** Whisper for transcription once archive exceeds 50-100 sermons
- **Consider:** PeerTube if video sermons are central to ministry strategy
- **Storage Planning:** Budget for expanding sermon archive (100-500GB typical)

### Large Churches (500+)

**Start Here:** Castopod or PeerTube (depending on audio vs. video focus)

- **Castopod** for audio-primary ministries with professional podcast presence
- **PeerTube** for video-primary ministries with live streaming needs
- **Add:** Whisper transcription pipeline for accessibility and searchability
- **Consider:** CDN integration for global reach and bandwidth management
- **Infrastructure:** Plan for dedicated server or managed hosting service

---

## Integration Notes

### With Church Websites

Most platforms provide embed codes or RSS feeds that integrate with WordPress, Wix, and static site generators. Castopod and PeerTube offer the most polished embed experiences.

### With Podcast Directories

Castopod generates standard RSS feeds for submission to Apple Podcasts, Spotify, Google Podcasts, and others. PeerTube can generate podcast feeds through plugins. Navidrome and Audiobookshelf do not support podcast directory distribution.

### With Transcription Workflows

Whisper integrates well with all platforms through file-based workflows. Process sermon audio through Whisper, then upload both audio and transcript to hosting platform. Some churches automate this with shell scripts or Python.

### With Cloud Storage

Most platforms support S3-compatible storage (Backblaze B2, Wasabi, MinIO) as alternative to local storage. This reduces server storage costs and improves global delivery performance.

### With Church Management Systems

ChurchApps provides native integration. Others typically integrate through RSS feeds, embeds, or API connections. Castopod supports webhook notifications for integration automation.

---

## Migration Considerations

**Moving From:**
- **YouTube:** PeerTube offers migration tools; expect to re-upload content
- **Libsyn/Buzzsprout:** Export RSS feed, download media files, import to Castopod
- **SoundCloud:** Download audio files manually, re-upload to self-hosted platform
- **Simplecast/Transistor:** Standard podcast migration via RSS and media downloads

**Preserving:**
- **Analytics history:** Export before migration; most platforms don't import historical data
- **Subscriber counts:** RSS feed URL changes may require re-subscription
- **Podcast directory listings:** Update feed URLs in Apple Podcasts, Spotify, etc.

---

## Common Deployment Patterns

**Pattern 1: Audio-Only Simple**
- Castopod on a small VPS (1 GB RAM is enough)
- Upload sermons weekly via web interface
- Automatic RSS feed generation + listener analytics
- Cost: $5-10/month

**Pattern 2: Professional Podcast**
- Castopod on VPS or managed Docker
- Submit to all major podcast directories
- Analytics for listener insights
- Cost: $10-20/month

**Pattern 3: Video + Live Streaming**
- PeerTube on dedicated server
- Live worship services + sermon archives
- Federation with sister churches
- Cost: $30-60/month

**Pattern 4: Complete Archive System**
- Castopod or PeerTube for distribution
- Whisper for transcription pipeline
- S3-compatible storage for media files
- CDN for global delivery
- Cost: $40-100/month depending on scale

---

## Cost Reality Check

**Self-Hosted Sermon Podcast:**
- VPS Hosting: $10-15/month (2GB RAM, 50GB storage)
- Domain: $12/year
- Storage Growth: +50-100GB/year (100 sermons)
- Bandwidth: Usually unlimited on VPS
- **Year 1 Total:** ~$150-200
- **Year 5 Total:** ~$750-1000 (assuming storage expansion)

**Commercial Alternative (Libsyn "Advanced" Plan):**
- $20/month = $240/year
- 1500MB upload limit/month
- **Year 5 Total:** $1,200

Self-hosting pays off after 12-18 months if you maintain the infrastructure. Commercial services make sense if you value convenience over cost and control.

---

## Success Criteria

You've chosen well if:

- Sermons remain accessible even if hosting company changes terms
- RSS feed works reliably across all major podcast platforms
- Members can easily find and stream sermon archives
- Storage costs remain predictable as archive grows
- Accessibility needs are met (transcripts, quality options)
- Technical maintenance fits your volunteer capacity
- Analytics provide ministry insights without privacy invasion

---

## Last Updated

2026-04-30

**Version:** 1.1
**Maintainer:** PAI System / Seven
**Next Review:** 2026-10-30 (6 months)

## If self-hosting is too much

- Castopod (above) offers official managed hosting — the same Podcasting 2.0 features without the server.
- A narrow paid podcast host with RSS portability beats a stale self-hosted archive; your feed URL and audio files are what matter, keep them exportable.
- A simple YouTube/podcast-app presence is fine while the archive is small — just keep your own copies of the files.
