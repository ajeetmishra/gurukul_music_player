$DT1 = Get-Date -UFormat "%Y-%m-%d"
Get-Content C:\gurukul_music_player\logs\$DT1.log -Wait -Tail 30