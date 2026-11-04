# Local Edge Data Storage & Privacy Policy

## Privacy-Preserving Architecture
As specified in the Siddaganga Institute of Technology project synopsis:
1. **Zero Continuous Cloud Streaming**: Video frames captured from the AR/VR glasses or webcam are processed strictly inside the local Raspberry Pi RAM.
2. **No Raw Video Persistence**: Unprocessed full-frame video is never stored to flash/disk.
3. **Facial Anonymization**: All preview frames and event snapshots undergo automated facial Gaussian blurring before presentation on worker dashboards or supervisor mobile interfaces.
4. **Minimal Event Retention**: Only essential event metadata (timestamp, violation type, severity, anonymized worker ID hash, confidence, corrective recommendation) is stored in SQLite `construction_safety.db`.
5. **Configurable Retention Purge**: Automated background policy purges records older than the configured threshold (default 14 days).
