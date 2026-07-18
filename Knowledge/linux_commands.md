# Linux Commands for Developers


---

# CHAPTER 1: ESSENTIAL COMMANDS

```bash
# Navigation
cd /path/to/dir          # Change directory
cd ..                    # Go up one level
cd ~                     # Go home
pwd                      # Print current directory
ls -la                   # List all files with details
ls -lh                   # Human-readable sizes

# File operations
cp file.txt backup.txt   # Copy
mv old.txt new.txt       # Move/rename
rm file.txt              # Delete file
rm -rf folder/           # Delete folder recursively
mkdir -p a/b/c           # Create nested directories
touch file.txt           # Create empty file
cat file.txt             # Print file content
head -20 file.txt        # First 20 lines
tail -f log.txt          # Follow log in real-time
wc -l file.txt           # Count lines

# Search
grep "pattern" file.txt              # Search in file
grep -r "pattern" ./                 # Search recursively
grep -rn "TODO" --include="*.py" .   # Search .py files with line numbers
find . -name "*.log" -mtime +7       # Find .log files older than 7 days
find . -type f -size +100M           # Find files larger than 100MB
which python3                         # Find executable location

# Permissions
chmod +x script.sh       # Make executable
chmod 755 file            # rwxr-xr-x
chmod 600 secret.key      # rw------- (only owner)
chown user:group file     # Change owner

# Disk
df -h                    # Disk space
du -sh */                # Folder sizes
du -sh . --max-depth=1   # Size of each subfolder

# Process management
ps aux                   # All processes
ps aux | grep python     # Find python processes
top                      # Live process monitor
htop                     # Better process monitor
kill PID                 # Kill by PID
kill -9 PID              # Force kill
pkill -f "python server" # Kill by name pattern
nohup command &          # Run in background (survives logout)

# Network
curl https://api.example.com           # HTTP GET
curl -X POST -d '{"key":"val"}' URL    # HTTP POST
wget https://example.com/file.zip      # Download file
ss -tlnp                               # Show listening ports
ping google.com                        # Test connectivity
ip addr                                # Show IP addresses

# System
uname -a                 # System info
free -h                  # RAM usage
uptime                   # System uptime
nvidia-smi               # GPU status

# Package management (Ubuntu/Debian)
sudo apt update          # Refresh package list
sudo apt install nginx   # Install package
sudo apt remove nginx    # Remove package
sudo apt autoremove      # Clean unused packages

# Systemd services
sudo systemctl start nginx       # Start
sudo systemctl stop nginx        # Stop
sudo systemctl restart nginx     # Restart
sudo systemctl status nginx      # Status
sudo systemctl enable nginx      # Auto-start on boot
sudo journalctl -u nginx -f     # Follow service logs
```


---

# CHAPTER 2: USEFUL COMBOS

```bash
# Find and replace in all files
find . -name "*.py" -exec sed -i 's/old/new/g' {} +

# Count lines of code
find . -name "*.py" -exec wc -l {} + | tail -1

# Watch a command (refresh every 2s)
watch -n 2 nvidia-smi

# Run command on file change
while inotifywait -e modify server.py; do systemctl restart myapp; done

# Create tar.gz backup
tar -czf backup-$(date +%Y%m%d).tar.gz ./project/

# SSH tunnel (access remote port locally)
ssh -L 8080:localhost:3000 user@server

# Rsync (fast file sync)
rsync -avz ./project/ user@server:/opt/project/

# Screen/tmux (persistent terminal sessions)
screen -S myserver            # Create named session
screen -r myserver            # Reattach
tmux new -s myserver          # Tmux alternative
```