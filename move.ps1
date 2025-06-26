$Signature = @"
[DllImport("user32.dll")]
public static extern IntPtr SendMessage(IntPtr hWnd, UInt32 Msg, IntPtr wParam, 
IntPtr lParam);

[DllImport("user32.dll")]
public static extern void mouse_event(Int32 dwFlags, Int32 dx, Int32 dy, Int32 dwData, UIntPtr dwExtraInfo);
"@

Try {
  $ShowWindowAsync = Add-Type -MemberDefinition $Signature -Name 
"Win32ShowWindowAsync" }#-Namespace Win32Functions -PassThru -ErrorAction Ignore }
Catch { }

$MONITOR_ON = -1;
$MONITOR_OFF = 2;
$MONITOR_STANBY = 1;

[System.Int64]$MOUSEEVENTF_MOVE = 0x0001;

[System.IntPtr]$HWND_BROADCAST = New-Object System.IntPtr(0xffff)
[System.UInt32]$WM_SYSCOMMAND = 0x0112
[System.IntPtr]$SC_MONITORPOWER = New-Object System.IntPtr(0xF170)

# this commands puts monitors to sleep
# $ShowWindowAsync::SendMessage($HWND_BROADCAST, $WM_SYSCOMMAND, $SC_MONITORPOWER, [System.IntPtr]$MONITOR_OFF);

# this command wakes monitors up
# $ShowWindowAsync::mouse_event($MOUSEEVENTF_MOVE, 0, 1, 0, [System.UIntPtr]::Zero);

$start_h = 5
$stop_h = 22
$x = $null
$wsh = New-Object -ComObject WScript.Shell

while ($true){
    $s = Get-Date
    if (($s.Hour -gt $start_h) -and ($s.Hour -lt $stop_h)) {
        [void][System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms')
        [System.Windows.Forms.SendKeys]::SendWait("%")

 #      $point = [System.Windows.Forms.Cursor]::Position
 #      $point.x+=1
 #      #write-host $point
 #      [System.Windows.Forms.Cursor]::Position = $point
 #      Start-Sleep -Seconds 1
 #      $point = [System.Windows.Forms.Cursor]::Position
 #      $point.x-=1
 #      [System.Windows.Forms.Cursor]::Position = $point
        Start-Sleep -Seconds 1
 #      $click = [System.Windows.Forms.MouseButtons]::XButton1
 #      Start-Sleep -Seconds 1
 #      $click = [System.Windows.Forms.MouseButtons]::Right
        #$ShowWindowAsync::mouse_event($MOUSEEVENTF_MOVE, 0, 1, 0, [System.UIntPtr]::Zero);
        $wsh.SendKeys('+{CapsLock}')
        $wsh.SendKeys('+{CapsLock}')

        if ($x -ne $s.Hour){ write-host -NoNewline -ForegroundColor Red "`nWork time " $s.Hour ' '}
        write-host -ForegroundColor Red -NoNewline '.' $s.Minute
        }
    else{
        if ($x -ne $s.Hour){write-host -NoNewline -ForegroundColor Green "`nSleep time" $s.Hour ' '}
        write-host -ForegroundColor Green -NoNewline '.' $s.Minute
        }
    $x = $s.Hour
    Start-Sleep -Seconds 120
}
