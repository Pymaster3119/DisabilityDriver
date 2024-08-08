import matplotlib.pyplot as plt

# Given dictionary
data = {
    'html': 1, 'head': 1, 'script': 59, 'meta': 86, 'link': 37, 'style': 9, 'title': 1, 'div': 1813,
    'iron-iconset-svg': 27, 'svg': 183, 'defs': 31, 'g': 394, 'path': 547, 'circle': 11, 'body': 1,
    'span': 350, 'iframe': 3, 'ytd-app': 1, 'yt-guide-manager': 1, 'yt-mdx-manager': 1, 'yt-playlist-manager': 1,
    'yt-hotkey-manager': 1, 'ytd-miniplayer': 1, 'yt-icon-button': 32, 'button': 99, 'yt-icon': 115,
    'yt-interaction': 53, 'h1': 6, 'a': 146, 'yt-formatted-string': 108, 'yt-attributed-string': 61,
    'ytd-badge-supported-renderer': 119, 'ytd-playlist-panel-renderer': 3, 'h3': 28, 'ytd-miniplayer-toast': 2,
    'ytd-thumbnail': 25, 'yt-image': 25, 'ytd-masthead': 1, 'iron-media-query': 6, 'tp-yt-paper-tooltip': 52,
    'ytd-topbar-logo-renderer': 2, 'ytd-logo': 4, 'ytd-yoodle-renderer': 2, 'picture': 2, 'source': 2,
    'img': 48, 'ytd-lottie-player': 2, 'ytd-button-renderer': 17, 'yt-button-shape': 43, 'yt-touch-feedback-shape': 43,
    'dom-if': 27, 'template': 135, 'ytd-searchbox': 1, 'form': 1, 'input': 2, 'ytd-topbar-menu-button-renderer': 1,
    'tp-yt-app-drawer': 1, 'ytd-mini-guide-renderer': 1, 'ytd-page-manager': 1, 'ytd-watch-flexy': 1,
    'player-microformat-renderer': 1, 'ytd-player': 2, 'video': 1, 'use': 32, 'label': 5, 'text': 9,
    'clippath': 17, 'yt-playability-error-supported-renderers': 1, 'ytd-engagement-panel-section-list-renderer': 3,
    'ytd-ads-engagement-panel-content-renderer': 1, 'ytd-engagement-panel-title-header-renderer': 2,
    'yt-img-shadow': 12, 'h2': 5, 'ytd-structured-description-content-renderer': 3, 'ytd-video-description-header-renderer': 1,
    'ytd-expandable-video-description-body-renderer': 1, 'ytd-expander': 1, 'tp-yt-paper-button': 7,
    'ytd-text-inline-expander': 2, 'dom-repeat': 108, 'ytd-horizontal-card-list-renderer': 2,
    'ytd-rich-list-header-renderer': 2, 'yt-video-attribute-view-model': 2, 'h4': 2, 'yt-button-view-model': 13,
    'button-view-model': 17, 'ytd-video-description-infocards-section-renderer': 2, 'ytd-compact-infocard-renderer': 8,
    'ytd-structured-description-video-lockup-renderer': 2, 'ytd-thumbnail-overlay-time-status-renderer': 20,
    'badge-shape': 20, 'ytd-structured-description-playlist-lockup-renderer': 6, 'yt-collections-stack': 8,
    'ytd-thumbnail-overlay-bottom-panel-renderer': 8, 'yt-sort-filter-sub-menu-renderer': 1, 'yt-dropdown-menu': 1,
    'tp-yt-paper-menu-button': 1, 'tp-yt-iron-dropdown': 1, 'tp-yt-paper-listbox': 1, 'tp-yt-paper-item': 2,
    'tp-yt-paper-item-body': 2, 'yt-reload-continuation': 2, 'ytd-section-list-renderer': 1, 'ytd-comments': 2,
    'tp-yt-paper-spinner-lite': 4, 'ytd-item-section-renderer': 2, 'ytd-continuation-item-renderer': 3,
    'tp-yt-paper-spinner': 3, 'polygon': 1, 'ytd-live-chat-frame': 1, 'ytd-message-renderer': 1,
    'ytd-toggle-button-renderer': 1, 'ytd-watch-metadata': 1, 'ytd-video-owner-renderer': 1, 'ytd-channel-name': 21,
    'ytd-subscribe-button-renderer': 1, 'yt-smartimation': 3, 'yt-animated-action': 1, 'lottie-component': 2,
    'rect': 62, 'mask': 17, 'lineargradient': 9, 'stop': 32, 'ytd-subscription-notification-toggle-button-renderer-next': 1,
    'ytd-menu-renderer': 20, 'segmented-like-dislike-button-view-model': 2, 'like-button-view-model': 2,
    'toggle-button-view-model': 4, 'dislike-button-view-model': 2, 'ytd-download-button-renderer': 2,
    'ytd-watch-info-text': 1, 'yt-animated-rolling-number': 2, 'ytd-metadata-row-container-renderer': 3,
    'ytd-video-primary-info-renderer': 1, 'ytd-video-view-count-renderer': 1, 'ytd-sentiment-bar-renderer': 1,
    'ytd-watch-next-secondary-results-renderer': 1, 'ytd-compact-radio-renderer': 2, 'ytd-thumbnail-overlay-now-playing-renderer': 20,
    'ytd-thumbnail-overlay-equalizer': 20, 'ytd-video-meta-block': 20, 'ytd-compact-video-renderer': 18, 'p': 6,
    'ytd-video-quality-promo-renderer': 1, 'yt-notification-action-renderer': 1, 'tp-yt-paper-toast': 1,
    'yt-button-renderer': 3, 'ytd-permission-role-bottom-bar-renderer': 1, 'ytd-popup-container': 1,
    'tp-yt-paper-dialog': 1, 'yt-mealbar-promo-renderer': 1, 'ytd-third-party-manager': 1, 'ytd-video-preview': 1,
    'yt-inline-player-controls': 1, 'yt-page-navigation-progress': 1, 'radialgradient': 4, 'iron-a11y-announcer': 1
}

# Create lists for tags and counts
tags = list(data.keys())
counts = list(data.values())

# Create the histogram
plt.figure(figsize=(12, 8))
plt.barh(tags, counts, color='skyblue')
plt.xlabel('Count')
plt.title('Histogram of Tags')
plt.gca().invert_yaxis()  # Invert y-axis to have the most frequent tags on top
plt.show()
