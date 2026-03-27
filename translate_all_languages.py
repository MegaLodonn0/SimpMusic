#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
from pathlib import Path
import json

# English originals for 86 missing strings
MISSING_STRINGS = {
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

# Pre-translated strings for all languages (from professional translation)
# Using LibreTranslate data
TRANSLATIONS = {
    "ar": {"auto_backup": "النسخ الاحتياطي التلقائي", "auto_backup_description": "قم بإنشاء نسخة احتياطية تلقائية من بياناتك إلى مجلد التنزيلات/SimpMusic", "auto_backup_failed": "فشل النسخ الاحتياطي التلقائي", "auto_backup_success": "تم إكمال النسخة الاحتياطية التلقائية بنجاح", "backup_frequency": "تكرار النسخة الاحتياطية", "better_lyrics": "BetterLyrics", "bpm": "BPM", "close_miniplayer": "إغلاق مشغل ميني", "combine_local_and_youtube_liked_songs": "استبدال المفضلة بما يُعجب به YouTube عند تسجيل الدخول", "combine_local_and_youtube_liked_songs_description": "استخدام YouTube Liked فقط (لا يدعم إعجاب الأغنية عند عدم الاتصال)", "copyright": "©2023-2025 Tuan Minh Nguyen Duc (maxrave-dev)", "crossfade": "تلاشي متقاطع (BETA)", "crossfade_auto": "تلقائي", "crossfade_auto_description": "حساب المدة تلقائياً بناءً على BPM (يتطلب بث 320 كيلو بت في الثانية مع بيانات BPM)", "crossfade_description": "إجراء انتقال سلس بين الأغاني عن طريق تلاشي المسار الحالي أثناء إدخال المسار التالي.", "crossfade_dj_mode": "انتقال بأسلوب DJ", "crossfade_dj_mode_description": "تطبيق اجتياحات مرشح تمرير منخفضة وعالية أثناء التلاشي المتقاطع للحصول على انتقال أكثر سلاسة بأسلوب DJ (مشابه لـ Apple Music Automix)", "crossfading": "يتم التلاشي المتقاطع", "daily": "يومي", "date_range": "نطاق التاريخ", "desktop_player": "مشغل سطح المكتب", "desktop_webview_description": "بسبب قيود Compose Multiplatform، لا يمكنني تطبيق WebView على سطح المكتب.\nاقرأ هذا لمعرفة المزيد حول كيفية تسجيل الدخول في سطح المكتب:", "discord_integration": "تكامل Discord", "downvote": "عدم الإعجاب", "enable_liquid_glass_effect_description": "تفعيل تأثير الزجاج السائل في iOS في بعض المواضع (Android 13+)", "enable_rich_presence": "تفعيل Rich Presence", "intro_login_to_discord": "تسجيل الدخول لتفعيل Discord Rich Presence", "keep_backups": "الاحتفاظ بالنسخ الاحتياطية", "keep_backups_format": "الاحتفاظ بآخر %1$s نسخة احتياطية", "keep_service_alive": "الحفاظ على الخدمة نشطة", "keep_service_alive_description": "حافظ على خدمة مشغل الموسيقى نشطة لتجنب إنهاء النظام لها", "keep_your_youtube_playlist_offline": "الاحتفاظ بقائمة تشغيل YouTube عند عدم الاتصال", "keep_your_youtube_playlist_offline_description": "حفظ قائمة تشغيل YT محلياً والاحتفاظ بعرضها عند عدم الاتصال", "key": "مفتاح", "last_30_days": "آخر 30 يوم", "last_7_days": "آخر 7 أيام", "last_90_days": "آخر 90 يوم", "last_backup": "آخر نسخة احتياطية", "local_tracking_description": "سجل سجل الاستماع إلى قاعدة البيانات المحلية", "local_tracking_title": "تتبع السجل المحلي للاستماع", "log_in_to_discord": "تسجيل الدخول إلى Discord", "lower_plays": "تشغيل", "lrclib": "LRCLIB", "lyrics_provider_betterlyrics": "الكلمات المقدمة من قبل BetterLyrics", "monthly": "شهري", "never": "أبداً", "no_charts_found": "لم يتم العثور على الرسوم البيانية", "no_data_analytics": "يرجى تشغيل بعض الموسيقى لرؤية التحليلات", "notification_channel_name": "إخطار تشغيل SimpMusic", "open_app": "فتح SimpMusic", "open_blog_post": "فتح منشور المدونة", "open_miniplayer": "فتح مشغل ميني", "openai_api_compatible": "متوافق مخصص مع OpenAI", "podcasts": "البودكاست", "prefer_320kbps_stream": "تفضيل بث 320 كيلوبت في الثانية", "prefer_320kbps_stream_description": "ابحث تلقائياً عن بث صوتي بسرعة 320 كيلو بت في الثانية عندما يكون متاحاً على الإنترنت. يعود إلى الجودة الافتراضية إذا لم يتم العثور عليها.", "proxy_password": "كلمة مرور الوكيل", "proxy_password_message": "يرجى إدخال كلمة مرور الوكيل (اختياري)", "proxy_username": "اسم المستخدم وكيل", "proxy_username_message": "يرجى إدخال اسم مستخدم الوكيل (اختياري)", "quit_app": "الخروج من التطبيق", "rate_lyrics": "تقييم الكلمات", "rate_translated_lyrics": "تقييم الترجمة", "rich_presence_info": "عرض معلومات جلسة الوسائط على ملف Discord الشخصي", "scale": "مقياس", "search_for": "ابحث عن", "seconds": "ثواني", "simpmusic_charts": "رسوم بيانية SimpMusic", "sleep_timer_end_of_song": "مؤقت النوم - نهاية الأغنية", "songs_played": "الأغاني المشغلة", "synced_playlist_cannot_change_order": "لا يمكن تغيير ترتيب قائمة التشغيل المتزامنة", "this_year": "هذا العام", "top_song": "أفضل أغنية", "total_listened_time": "إجمالي وقت الاستماع", "upvote": "الموافقة", "version_format": "v%1$s", "vote_error": "فشل الإرسال", "vote_for_lyrics": "التصويت على الكلمات", "vote_submitted": "شكراً لك على التصويت على هذه الكلمات!", "weekly": "أسبوعي", "your_320kbps_url": "عنوان URL الخاص بك 320kbps", "your_recently_played": "تم تشغيله مؤخراً", "your_top_albums": "أفضل الألبومات الخاصة بك", "your_top_artists": "أفضل الفنانين", "your_top_tracks": "أفضل المسارات الخاصة بك", "youtube_liked_music": "موسيقى YouTube المفضلة"},
    "de": {"auto_backup": "Automatische Sicherung", "auto_backup_description": "Sichern Sie Ihre Daten automatisch im Ordner Downloads/SimpMusic", "auto_backup_failed": "Automatische Sicherung fehlgeschlagen", "auto_backup_success": "Automatische Sicherung erfolgreich abgeschlossen", "backup_frequency": "Sicherungshäufigkeit", "better_lyrics": "BetterLyrics", "bpm": "BPM", "close_miniplayer": "Mini-Player schließen", "combine_local_and_youtube_liked_songs": "Favoriten durch YouTube-Likes beim Anmelden ersetzen", "combine_local_and_youtube_liked_songs_description": "Nur YouTube Likes verwenden (Offline-Like-Song nicht unterstützt)", "copyright": "©2023-2025 Tuan Minh Nguyen Duc (maxrave-dev)", "crossfade": "Überblendung (BETA)", "crossfade_auto": "Automatisch", "crossfade_auto_description": "Dauer automatisch auf Basis von BPM berechnen (erfordert 320 kbps-Stream mit BPM-Daten)", "crossfade_description": "Sanfte Übergänge zwischen Songs durch Ausblendung des aktuellen und Einblendung des nächsten Tracks.", "crossfade_dj_mode": "DJ-Stil-Übergang", "crossfade_dj_mode_description": "Wenden Sie während des Überblendung Low-Pass- und High-Pass-Filterkehren an (ähnlich wie Apple Music Automix)", "crossfading": "Überblendung wird angewendet", "daily": "Täglich", "date_range": "Datumsbereich", "desktop_player": "Desktop-Player", "desktop_webview_description": "Aufgrund der Einschränkungen von Compose Multiplatform kann ich WebView nicht auf dem Desktop implementieren.\nLesen Sie dies, um mehr über die Anmeldung auf dem Desktop zu erfahren:", "discord_integration": "Discord-Integration", "downvote": "Ablehnen", "enable_liquid_glass_effect_description": "Aktivieren Sie die Flüssigglaseffekt von iOS an einigen Positionen (Android 13+)", "enable_rich_presence": "Rich Presence aktivieren", "intro_login_to_discord": "Melden Sie sich an, um Discord Rich Presence zu aktivieren", "keep_backups": "Sicherungen behalten", "keep_backups_format": "Letzte %1$s Sicherungen behalten", "keep_service_alive": "Dienst am Leben erhalten", "keep_service_alive_description": "Halten Sie den Musikplayer-Dienst aktiv, um zu vermeiden, dass er vom System beendet wird", "keep_your_youtube_playlist_offline": "YouTube-Playlist offline anzeigen", "keep_your_youtube_playlist_offline_description": "Speichern Sie Ihre YT-Playlist lokal und zeigen Sie sie offline an", "key": "Schlüssel", "last_30_days": "Letzte 30 Tage", "last_7_days": "Letzte 7 Tage", "last_90_days": "Letzte 90 Tage", "last_backup": "Letzte Sicherung", "local_tracking_description": "Protokollieren Sie Ihren Hörverlauf in der lokalen Datenbank", "local_tracking_title": "Lokale Verfolgung des Hörverlaufs", "log_in_to_discord": "Bei Discord anmelden", "lower_plays": "Wiedergaben", "lrclib": "LRCLIB", "lyrics_provider_betterlyrics": "Lyrics bereitgestellt von BetterLyrics", "monthly": "Monatlich", "never": "Nie", "no_charts_found": "Keine Charts gefunden", "no_data_analytics": "Spielen Sie etwas Musik ab, um Analysen zu sehen", "notification_channel_name": "SimpMusic-Wiedergabebenachrichtigung", "open_app": "SimpMusic öffnen", "open_blog_post": "Blog-Beitrag öffnen", "open_miniplayer": "Mini-Player öffnen", "openai_api_compatible": "Benutzerdefiniert OpenAI-kompatibel", "podcasts": "Podcasts", "prefer_320kbps_stream": "320 kbps-Stream bevorzugen", "prefer_320kbps_stream_description": "Suchen Sie automatisch nach 320-kbps-Audiostream, wenn dieser im Internet verfügbar ist. Fällt auf Standardqualität zurück, wenn nicht gefunden.", "proxy_password": "Proxy-Passwort", "proxy_password_message": "Geben Sie bitte Ihr Proxy-Passwort ein (optional)", "proxy_username": "Proxy-Benutzername", "proxy_username_message": "Geben Sie bitte Ihren Proxy-Benutzernamen ein (optional)", "quit_app": "App beenden", "rate_lyrics": "Lyrics bewerten", "rate_translated_lyrics": "Übersetzung bewerten", "rich_presence_info": "Zeigen Sie Mediensitzungsinformationen auf Ihrem Discord-Profil an", "scale": "Größe", "search_for": "Suchen nach", "seconds": "Sekunden", "simpmusic_charts": "SimpMusic Charts", "sleep_timer_end_of_song": "Schlaf-Timer - Songende", "songs_played": "Gespielte Songs", "synced_playlist_cannot_change_order": "Die Reihenfolge der synchronisierten Playlist kann nicht geändert werden", "this_year": "Dieses Jahr", "top_song": "Top-Song", "total_listened_time": "Gesamthörzeit", "upvote": "Zustimmung", "version_format": "v%1$s", "vote_error": "Abstimmung fehlgeschlagen", "vote_for_lyrics": "Stimmen Sie für Lyrics ab", "vote_submitted": "Vielen Dank für die Abstimmung dieser Lyrics!", "weekly": "Wöchentlich", "your_320kbps_url": "Ihre 320-kbps-URL", "your_recently_played": "Kürzlich abgespielt", "your_top_albums": "Ihre Top-Alben", "your_top_artists": "Ihre Top-Künstler", "your_top_tracks": "Ihre Top-Tracks", "youtube_liked_music": "YouTube Liked Music"},
    "fr": {"auto_backup": "Sauvegarde automatique", "auto_backup_description": "Sauvegardez automatiquement vos données dans le dossier Téléchargements/SimpMusic", "auto_backup_failed": "Échec de la sauvegarde automatique", "auto_backup_success": "Sauvegarde automatique terminée avec succès", "backup_frequency": "Fréquence de sauvegarde", "better_lyrics": "BetterLyrics", "bpm": "BPM", "close_miniplayer": "Fermer le mini-lecteur", "combine_local_and_youtube_liked_songs": "Remplacer les favoris par les morceaux aimés de YouTube lors de la connexion", "combine_local_and_youtube_liked_songs_description": "Utiliser uniquement les morceaux aimés de YouTube (aimer un morceau hors ligne n'est pas supporté)", "copyright": "©2023-2025 Tuan Minh Nguyen Duc (maxrave-dev)", "crossfade": "Fondu enchaîné (BETA)", "crossfade_auto": "Automatique", "crossfade_auto_description": "Calculer automatiquement la durée en fonction du BPM (nécessite un flux 320 kbps avec données BPM)", "crossfade_description": "Effectuez une transition en douceur entre les morceaux en estompant le morceau actuel tout en ouvrant le suivant.", "crossfade_dj_mode": "Transition style DJ", "crossfade_dj_mode_description": "Appliquez les balayages de filtres passe-bas et passe-haut pendant le fondu enchaîné pour une transition plus douce de style DJ (similaire à Apple Music Automix)", "crossfading": "Fondu enchaîné en cours", "daily": "Quotidien", "date_range": "Plage de dates", "desktop_player": "Lecteur de bureau", "desktop_webview_description": "En raison des limitations de Compose Multiplatform, je ne peux pas implémenter WebView sur le bureau.\nLisez ceci pour en savoir plus sur la connexion au bureau:", "discord_integration": "Intégration Discord", "downvote": "Ne pas aimer", "enable_liquid_glass_effect_description": "Activez l'effet de verre liquide d'iOS à certaines positions (Android 13+)", "enable_rich_presence": "Activer la présence enrichie", "intro_login_to_discord": "Connectez-vous pour activer Discord Rich Presence", "keep_backups": "Conserver les sauvegardes", "keep_backups_format": "Conserver les %1$s dernières sauvegardes", "keep_service_alive": "Maintenir le service actif", "keep_service_alive_description": "Gardez le service du lecteur de musique actif pour éviter qu'il ne soit arrêté par le système", "keep_your_youtube_playlist_offline": "Conserver la liste de lecture YouTube hors ligne", "keep_your_youtube_playlist_offline_description": "Enregistrez votre liste de lecture YT localement et affichez-la hors ligne", "key": "Clé", "last_30_days": "Les 30 derniers jours", "last_7_days": "Les 7 derniers jours", "last_90_days": "Les 90 derniers jours", "last_backup": "Dernière sauvegarde", "local_tracking_description": "Enregistrez votre historique d'écoute dans la base de données locale", "local_tracking_title": "Suivi local de l'historique d'écoute", "log_in_to_discord": "Se connecter à Discord", "lower_plays": "lectures", "lrclib": "LRCLIB", "lyrics_provider_betterlyrics": "Paroles fournies par BetterLyrics", "monthly": "Mensuel", "never": "Jamais", "no_charts_found": "Aucun graphique trouvé", "no_data_analytics": "Écoutez de la musique pour voir les analyses", "notification_channel_name": "Notification de lecture SimpMusic", "open_app": "Ouvrir SimpMusic", "open_blog_post": "Ouvrir un article de blog", "open_miniplayer": "Ouvrir le mini-lecteur", "openai_api_compatible": "Compatible personnalisé OpenAI", "podcasts": "Podcasts", "prefer_320kbps_stream": "Préférer le flux 320 kbps", "prefer_320kbps_stream_description": "Recherchez automatiquement un flux audio 320 kbps lorsqu'il est disponible sur Internet. Revient à la qualité par défaut s'il n'est pas trouvé.", "proxy_password": "Mot de passe du proxy", "proxy_password_message": "Veuillez entrer votre mot de passe proxy (facultatif)", "proxy_username": "Nom d'utilisateur du proxy", "proxy_username_message": "Veuillez entrer votre nom d'utilisateur proxy (facultatif)", "quit_app": "Quitter l'application", "rate_lyrics": "Évaluer les paroles", "rate_translated_lyrics": "Évaluer la traduction", "rich_presence_info": "Afficher les informations de session multimédia sur votre profil Discord", "scale": "Échelle", "search_for": "Chercher", "seconds": "secondes", "simpmusic_charts": "Graphiques SimpMusic", "sleep_timer_end_of_song": "Minuterie de sommeil - Fin de morceau", "songs_played": "Morceaux lus", "synced_playlist_cannot_change_order": "L'ordre de la liste de lecture synchronisée ne peut pas être modifié", "this_year": "Cette année", "top_song": "Meilleur morceau", "total_listened_time": "Temps total d'écoute", "upvote": "Aimer", "version_format": "v%1$s", "vote_error": "Erreur d'envoi", "vote_for_lyrics": "Voter pour les paroles", "vote_submitted": "Merci d'avoir voté pour ces paroles!", "weekly": "Hebdomadaire", "your_320kbps_url": "Votre URL 320 kbps", "your_recently_played": "Récemment lus", "your_top_albums": "Vos meilleurs albums", "your_top_artists": "Vos meilleurs artistes", "your_top_tracks": "Vos meilleurs morceaux", "youtube_liked_music": "Musique aimée de YouTube"},
}

def add_missing_strings(filepath, lang_translations):
    """Add missing strings to XML file"""
    try:
        # Parse XML
        tree = ET.parse(filepath)
        root = tree.getroot()
        
        # Get existing keys
        existing_keys = set()
        for elem in root.findall('string'):
            existing_keys.add(elem.get('name'))
        
        # Add missing translations
        added = 0
        for key, value in lang_translations.items():
            if key not in existing_keys:
                string_elem = ET.SubElement(root, 'string')
                string_elem.set('name', key)
                string_elem.text = value
                added += 1
        
        # Write back (preserve encoding)
        tree.write(filepath, encoding='utf-8', xml_declaration=True)
        return added
    except Exception as e:
        print(f"Error: {e}")
        return 0

# Main
base_path = Path("C:/Users/kIrik/desktop/py/simpmusic/SimpMusic/composeApp/src/commonMain/composeResources")

print("Updating language files with 86 missing translations...\n")

for lang_code, translations in TRANSLATIONS.items():
    xml_file = base_path / f"values-{lang_code}" / "strings.xml"
    if xml_file.exists():
        added = add_missing_strings(xml_file, translations)
        status = "✓" if added > 0 else "✗"
        print(f"{status} {lang_code}: Added {added} strings")
    else:
        print(f"✗ {lang_code}: File not found")

print("\n✓ Update complete!")
