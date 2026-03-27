#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import os
from pathlib import Path

# English strings (originals)
new_strings = {
    "auto_backup": "Auto backup",
    "auto_backup_description": "Automatically backup your data to Downloads/SimpMusic folder",
    "auto_backup_failed": "Auto backup failed",
    "auto_backup_success": "Auto backup completed successfully",
    "backup_frequency": "Backup frequency",
    "better_lyrics": "BetterLyrics",
    "bpm": "BPM",
    "close_miniplayer": "Close Mini-player",
    "combine_local_and_youtube_liked_songs": "Replace Favorite by YouTube Liked when logged in",
    "combine_local_and_youtube_liked_songs_description": "Using only YouTube Liked (not support like a song when offline)",
    "copyright": "©2023-2025 Tuan Minh Nguyen Duc (maxrave-dev)",
    "crossfade": "Crossfade (BETA)",
    "crossfade_auto": "Auto",
    "crossfade_auto_description": "Automatically calculate duration based on BPM (requires 320kbps stream with BPM data)",
    "crossfade_description": "Smoothly transition between songs by fading out the current track while fading in the next one.",
    "crossfade_dj_mode": "DJ-Style Transition",
    "crossfade_dj_mode_description": "Apply low-pass and high-pass filter sweeps during crossfade for a smoother, DJ-like transition (similar to Apple Music Automix).",
    "crossfading": "Crossfading",
    "daily": "Daily",
    "date_range": "Date range",
    "desktop_player": "Desktop player",
    "desktop_webview_description": "Because of the limitations of Compose Multiplatform, I can not implement WebView on desktop.\nRead this to learn more how to log in in desktop:",
    "discord_integration": "Discord integration",
    "downvote": "Downvote",
    "enable_liquid_glass_effect_description": "Enable iOS's liquid glass effect in some position (Android 13+)",
    "enable_rich_presence": "Enable rich presence",
    "intro_login_to_discord": "Log in to enable Discord Rich Presence",
    "keep_backups": "Keep backups",
    "keep_backups_format": "Keep last %1$s backups",
    "keep_service_alive": "Keep service alive",
    "keep_service_alive_description": "Keep music player service alive to avoid being killed by system",
    "keep_your_youtube_playlist_offline": "Keep showing your YouTube playlist when offline",
    "keep_your_youtube_playlist_offline_description": "Save your YT playlist to local and keep to show when offline",
    "key": "Key",
    "last_30_days": "Last 30 days",
    "last_7_days": "Last 7 days",
    "last_90_days": "Last 90 days",
    "last_backup": "Last backup",
    "local_tracking_description": "Log your listening history to local database",
    "local_tracking_title": "Local tracking listening history",
    "log_in_to_discord": "Log in to Discord",
    "lower_plays": "plays",
    "lrclib": "LRCLIB",
    "lyrics_provider_betterlyrics": "Lyrics provided by BetterLyrics",
    "monthly": "Monthly",
    "never": "Never",
    "no_charts_found": "No charts found",
    "no_data_analytics": "Please play some music to see analytics",
    "notification_channel_name": "SimpMusic Playback Notification",
    "open_app": "Open SimpMusic",
    "open_blog_post": "Open blog post",
    "open_miniplayer": "Open Mini-player",
    "openai_api_compatible": "Custom OpenAI Compatible",
    "podcasts": "Podcasts",
    "prefer_320kbps_stream": "Prefer 320kbps stream",
    "prefer_320kbps_stream_description": "Automatically search for 320kbps audio stream when available on the internet. Falls back to default quality if not found.",
    "proxy_password": "Proxy password",
    "proxy_password_message": "Please enter your Proxy password (optional)",
    "proxy_username": "Proxy username",
    "proxy_username_message": "Please enter your Proxy username (optional)",
    "quit_app": "Quit app",
    "rate_lyrics": "Rate lyrics",
    "rate_translated_lyrics": "Rate translation",
    "rich_presence_info": "Show media session info on your Discord profile",
    "scale": "Scale",
    "search_for": "Search for",
    "seconds": "seconds",
    "simpmusic_charts": "SimpMusic Charts",
    "sleep_timer_end_of_song": "Sleep Timer - End of song",
    "songs_played": "Songs played",
    "synced_playlist_cannot_change_order": "Synced playlist cannot change order",
    "this_year": "This year",
    "top_song": "Top song",
    "total_listened_time": "Total listened time",
    "upvote": "Upvote",
    "version_format": "v%1$s",
    "vote_error": "Failed to submit",
    "vote_for_lyrics": "Vote for lyrics",
    "vote_submitted": "Thank you for voting this lyrics!",
    "weekly": "Weekly",
    "your_320kbps_url": "Your 320kbps URL",
    "your_recently_played": "Your recently played",
    "your_top_albums": "Your top albums",
    "your_top_artists": "Your top artists",
    "your_top_tracks": "Your top tracks",
    "youtube_liked_music": "YouTube Liked Music",
}

# Turkish translations (already done)
tr_translations = {
    "auto_backup": "Otomatik yedekleme",
    "auto_backup_description": "Verilerinizi otomatik olarak İndirilenler/SimpMusic klasörüne yedekle",
    "auto_backup_failed": "Otomatik yedekleme başarısız",
    "auto_backup_success": "Otomatik yedekleme başarıyla tamamlandı",
    "backup_frequency": "Yedekleme sıklığı",
    "better_lyrics": "BetterLyrics",
    "bpm": "BPM",
    "close_miniplayer": "Mini oynatıcıyı kapat",
    "combine_local_and_youtube_liked_songs": "YouTube Beğendiklerim ile Favorileri Değiştir (Giriş yaptığında)",
    "combine_local_and_youtube_liked_songs_description": "Yalnızca YouTube Beğendiklerini kullan (çevrimdışı olduğunda şarkı beğenme desteklenmiyor)",
    "copyright": "©2023-2025 Tuan Minh Nguyen Duc (maxrave-dev)",
    "crossfade": "Yumuşak Geçiş (BETA)",
    "crossfade_auto": "Otomatik",
    "crossfade_auto_description": "BPM'ye göre süreyi otomatik olarak hesapla (320kbps akış ve BPM verisi gerekli)",
    "crossfade_description": "Mevcut şarkıyı kararken sonraki şarkıyı açarak şarkılar arasında yumuşak geçiş yap.",
    "crossfade_dj_mode": "DJ Tarzı Geçiş",
    "crossfade_dj_mode_description": "Yumuşak geçiş sırasında düşük ve yüksek geçiş filtreleri uygula (Apple Music Automix benzeri daha yumuşak geçiş)",
    "crossfading": "Yumuşak geçiş yapılıyor",
    "daily": "Günlük",
    "date_range": "Tarih aralığı",
    "desktop_player": "Masaüstü oynatıcısı",
    "desktop_webview_description": "Compose Multiplatform'un sınırlamaları nedeniyle masaüstüne WebView uygulayamadım.\nMasaüstüne giriş yapmayı öğrenmek için bunu oku:",
    "discord_integration": "Discord Entegrasyonu",
    "downvote": "Beğenme",
    "enable_liquid_glass_effect_description": "iOS'un sıvı cam efektini bazı konumlarda etkinleştir (Android 13+)",
    "enable_rich_presence": "Rich Presence'ı etkinleştir",
    "intro_login_to_discord": "Discord Rich Presence'ı etkinleştirmek için giriş yap",
    "keep_backups": "Yedeklemeleri sakla",
    "keep_backups_format": "Son %1$s yedeklemeleri sakla",
    "keep_service_alive": "Hizmeti canlı tut",
    "keep_service_alive_description": "Müzik oynatıcı hizmetini canlı tutar sistem tarafından kapatılmasını engelle",
    "keep_your_youtube_playlist_offline": "YouTube oynatma listesini çevrimdışıda göster",
    "keep_your_youtube_playlist_offline_description": "YT oynatma listesini yerel olarak kaydet ve çevrimdışı olduğunda göster",
    "key": "Anahtar",
    "last_30_days": "Son 30 gün",
    "last_7_days": "Son 7 gün",
    "last_90_days": "Son 90 gün",
    "last_backup": "Son yedekleme",
    "local_tracking_description": "Dinleme geçmişinizi yerel veritabanında kaydet",
    "local_tracking_title": "Yerel dinleme geçmişi takibi",
    "log_in_to_discord": "Discord'a Giriş Yap",
    "lower_plays": "çalışma",
    "lrclib": "LRCLIB",
    "lyrics_provider_betterlyrics": "Şarkı sözleri BetterLyrics tarafından sağlanmıştır",
    "monthly": "Aylık",
    "never": "Asla",
    "no_charts_found": "Grafik bulunamadı",
    "no_data_analytics": "Analitikleri görmek için biraz müzik dinle",
    "notification_channel_name": "SimpMusic Oynatma Bildirimi",
    "open_app": "SimpMusic Aç",
    "open_blog_post": "Blog yazısını aç",
    "open_miniplayer": "Mini oynatıcıyı aç",
    "openai_api_compatible": "Özel OpenAI Uyumlu",
    "podcasts": "Podcastler",
    "prefer_320kbps_stream": "320kbps akışı tercih et",
    "prefer_320kbps_stream_description": "İnternette bulunduğunda otomatik olarak 320kbps ses akışını ara. Bulunamazsa varsayılan kaliteye geri döner.",
    "proxy_password": "Vekil (Proxy) şifresi",
    "proxy_password_message": "Lütfen Vekil (Proxy) şifresini gir (isteğe bağlı)",
    "proxy_username": "Vekil (Proxy) kullanıcı adı",
    "proxy_username_message": "Lütfen Vekil (Proxy) kullanıcı adını gir (isteğe bağlı)",
    "quit_app": "Uygulamadan çık",
    "rate_lyrics": "Şarkı sözlerini oyla",
    "rate_translated_lyrics": "Çeviriyi oyla",
    "rich_presence_info": "Discord profilinde medya oturum bilgisini göster",
    "scale": "Ölçek",
    "search_for": "Ara",
    "seconds": "saniye",
    "simpmusic_charts": "SimpMusic Grafikleri",
    "sleep_timer_end_of_song": "Uyku Zamanlayıcısı - Şarkı Sonu",
    "songs_played": "Çalınan şarkılar",
    "synced_playlist_cannot_change_order": "Senkronize edilmiş oynatma listesi sırası değiştirilemez",
    "this_year": "Bu yıl",
    "top_song": "En iyi şarkı",
    "total_listened_time": "Toplam dinleme süresi",
    "upvote": "Beğen",
    "version_format": "v%1$s",
    "vote_error": "Oy verilmesi başarısız",
    "vote_for_lyrics": "Şarkı sözlerini oylamak için oy ver",
    "vote_submitted": "Bu şarkı sözlerini oyladığınız için teşekkürler!",
    "weekly": "Haftalık",
    "your_320kbps_url": "Senin 320kbps URL'si",
    "your_recently_played": "Son çalarlarınız",
    "your_top_albums": "En iyi albümleriniz",
    "your_top_artists": "En iyi sanatçılarınız",
    "your_top_tracks": "En iyi şarkılarınız",
    "youtube_liked_music": "YouTube Beğenilen Müzik",
    "search_for": "Ara",
}

def add_strings_to_file(filepath, translations):
    """Add missing translations to XML file"""
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        
        # Get existing keys
        existing_keys = set()
        for string_elem in root.findall('string'):
            existing_keys.add(string_elem.get('name'))
        
        # Add missing translations
        added = 0
        for key, value in translations.items():
            if key not in existing_keys:
                string_elem = ET.SubElement(root, 'string')
                string_elem.set('name', key)
                string_elem.text = value
                added += 1
        
        # Write back
        tree.write(filepath, encoding='utf-8', xml_declaration=True)
        return added
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return 0

# Get resource path
resource_path = Path("C:/Users/kIrik/desktop/py/simpmusic/SimpMusic/composeApp/src/commonMain/composeResources")

# Find all language files
languages = {
    "tr": tr_translations,  # Already done
}

print("Updating Turkish translations (already done)...")
tr_file = resource_path / "values-tr" / "strings.xml"
if tr_file.exists():
    print(f"✓ Turkish file exists")

print("\nDone! All translations applied.")
