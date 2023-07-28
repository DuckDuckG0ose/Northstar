@echo off
title Windows Modding Tool
setlocal EnableDelayedExpansion

rem BatchGotAdmin
:-------------------------------------
REM  --> Check for permissions
    IF "%PROCESSOR_ARCHITECTURE%" EQU "amd64" (
>nul 2>&1 "%SYSTEMROOT%\SysWOW64\cacls.exe" "%SYSTEMROOT%\SysWOW64\config\system"
) ELSE (
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
)

REM --> If error flag set, we do not have admin.
if '%errorlevel%' NEQ '0' (
    @echo. & @echo. & @echo [1m[31mRequesting administrative privileges...[0m
	TIMEOUT -T 3 /nobreak >nul
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    set params= %*
    echo UAC.ShellExecute "cmd.exe", "/c ""%~s0"" %params:"=""%", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B
	

:gotAdmin
rem :To CD to the location of the batch script file (%0)
CD /d "%~dp0"

powershell.exe "Set-ExecutionPolicy Unrestricted -force" >nul

cls
@echo. & @echo [1m[34mCreate restore Point before advance.[0m
call %systemroot%\System32\SystemPropertiesProtection.exe

@echo [34mImport power settings mod, in power settings advanced settings will unlock more settings expecially in cpu option...[0m
@echo y|REG IMPORT "%~dp0dir\PowerManagementSetConf.reg" >nul

@echo [34mImport Visual Effects.[0m
@echo y|REG IMPORT "%~dp0dir\VisualEffects.reg" >nul

@echo. & @echo [34mKeybord speed tweak.[0m
@echo y|REG IMPORT "%~dp0dir\Keyboard.reg" >nul

@echo. & @echo [34mDisabling Cortana.[0m
@echo y|REG IMPORT "%~dp0dir\Disabling_Cortana.reg" >nul

@echo. & @echo [34mmouse speed tweak.[0m
@echo y|REG IMPORT "%~dp0dir\mouse.reg" >nul

@echo. & @echo [34mEnable old Photo viewer.[0m
@echo y|REG IMPORT "%~dp0dir\Enable_Photo_viewer.reg" >nul

@echo. & @echo [34mSetting MTU to 1492 PPPoE - Ethernet II MTU (1500) less PPPoE header (8). Big MTU has some downsides if the network transmission is not so stable.[0m
powershell.exe New-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters -Name MTU -PropertyType dword -Value 1492 -force
powershell.exe "Get-Item -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces\*"|New-ItemProperty -Name MTU -PropertyType dword -Value 1492 -force" 
powershell.exe "Get-Item -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip6\Parameters\Interfaces\*"|New-ItemProperty -Name MTU -PropertyType dword -Value 1492 -force"
powershell.exe "Get-Item -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Netbt\Parameters\Interfaces\*"|New-ItemProperty -Name MTU -PropertyType dword -Value 1492 -force"
powershell.exe "Get-Item -Path "HKLM:\SYSTEM\CurrentControlSet\Services\AFD\Parameters"|New-ItemProperty -Name FastSendDatagramThreshold -PropertyType dword -Value 1492 -force"
powershell.exe New-Item -Path 'HKLM:\SOFTWARE\Microsoft' -Name 'MSMQ' -ErrorAction SilentlyContinue >nul >nul
powershell.exe New-Item -Path 'HKLM:\SOFTWARE\Microsoft\MSMQ' -Name 'Parameters' -ErrorAction SilentlyContinue >nul >nul
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\MSMQ\Parameters' -Name MTU -PropertyType dword -Value 1492 -force

rem @echo. & @echo [34mEnabling Teredo tecnologie.[0m & @echo.
rem netsh interface teredo set state client

@echo [34mCleanning Dns Client Cache[0m
powershell.exe Clear-DnsClientCache

@echo [34mWinsock autotuning on.[0m & @echo.
netsh winsock set autotuning on

@echo [34mEnable tcp window heuristics.[0m & @echo.
set heuristics enabled enabled
set heuristics wsh=enabled forcews=enabled

@echo [34mEnable Fastopen, Rss, Dca, disable ecncapability.[0m & @echo.
netsh int tcp set global fastopen=enabled ecncapability=disabled rss=enabled dca=enabled

@echo [34mNon Sack Rtt Resiliency, "disabled" for stable connections, "enabled" for connections with fluctuating ping and in the presence of packet loss. State=Enabled[0m & @echo.
netsh int tcp set global nonsackrttresiliency=enabled

@echo [34mTCP memory pressure protection helps ensure that a computer continues normal operation when low on memory due to denial of service attacks. State Enabled.[0m & @echo.
powershell.exe Set-NetTCPSetting -MemoryPressureProtection Enabled

@echo [34mTimestamps facilitate round trip measurement. Disabling TCP timestamp may cause some performance issues. State Enabled[0m & @echo.
powershell.exe Set-NetTCPSetting -Timestamps Enable

@echo [34mMax SYN Retransmissions, sets the number of times to attempt to reestablish a connection with SYN packets. Times set to 3.[0m & @echo.
powershell.exe Set-NetTCPSetting -SettingName InternetCustom -MaxSynRetransmissions 3

@echo [34mInternet congestionprovider=CUBIC.[0m & @echo.
netsh int tcp set supplemental template=internet congestionprovider=CUBIC
powershell.exe Set-NetTCPSetting -SettingName "InternetCustom" -CongestionProvider CUBIC

@echo [34mChimney Disabled PacketCoalescingFilter enabled.[0m & @echo.
powershell.exe Set-NetOffloadGlobalSetting -Chimney Disabled

@echo [34mPacketCoalescingFilter enabled for pure throughput when lower CPU utilization is important.[0m & @echo.
powershell.exe Set-NetOffloadGlobalSetting -PacketCoalescingFilter enabled

@echo [34mScalingHeuristics Disabled.[0m & @echo.
powershell.exe Set-NetTCPSetting -SettingName InternetCustom -ScalingHeuristics Disabled

rem		AutoTuningLevel	     scale Factor  	scale multiplier                       Window size formula
rem        Disabled	            0	                   0	                         window size
rem        Restricted          	4	                 2^4	                         window size * (2^4)
rem     Highly restricted	    2	                 2^2	                         window size * (2^2)
rem         Normal	            8	                 2^8	                         window size * (2^8)
rem      Experimental	       14	                 2^14                            window size * (2^14)

@echo [34m Setting autotuninglevel to Restricted.[0m & @echo.
netsh int tcp set global autotuninglevel=Restricted

@echo [34mNetwork direct memory acess ON. Not work together with Chimney Offload but Chimney Offload is out since Windows 10.[0m & @echo.
netsh int tcp set global netdma=enabled

@echo [34mEnable Receive Side Scaling (RSS). Receive-side scaling setting enables parallelized processing of received packets on multiple processors.[0m & @echo.
netsh int tcp set global rss = enabled
powershell.exe Set-NetAdapterRss -Name * -Enabled $True -IncludeHidden

@echo [34mDisable Receive Segment Coalescing State (RSC) for pure gaming latency.[0m& @echo.
netsh int tcp set global rsc = disable
powershell.exe Disable-NetAdapterRsc -Name * -IncludeHidden

@echo [34mSet IPV4 IPV6 RSC for Adapters.[0m & @echo.
powershell.exe Set-NetAdapterRsc -Name * -IncludeHidden -IPv4Enabled $True -IPv6Enabled $True

@echo [34mSet an RSS profile for a NUMA server without dynamic load balancing, Base Processor Number 0, Max Processor Number 1,Max Processors 2, -NumberOfReceiveQueues 2.[0m & @echo.
powershell.exe Set-NetAdapterRss -Name * -Profile NUMAStatic -BaseProcessorNumber 0 -MaxProcessorNumber 1 -MaxProcessors 2 -NumberOfReceiveQueues 2 -IncludeHidden

@echo [34mEnabling Adapter Checksum Offload.[0m & @echo.
powershell.exe Enable-NetAdapterChecksumOffload -Name * -TcpIPv6 -UdpIPv6 -TcpIPv4 -UdpIPv4 -IpIPv4 -IncludeHidden

@echo [34mEnable Large Send Offload (LSO)This setting enables Large Send Offload. When enabled, the network adapter hardware is used to complete data segmentation, 
@echo theoretically faster than operating system software. Theoretically, this feature may improve transmission performance, and reduce CPU load.[0m & @echo.
powershell.exe Enable-NetAdapterLso -Name * -IncludeHidden

@echo [34met-NetAdapterLso cmdlet manages the large send offload property which can improve send side performance by having the network adapter distribute a large send request into smaller sizes that can be sent out by the network adapter.[0m & @echo.
powershell.exe set-NetAdapterLso -Name * -IncludeHidden -IPv4Enabled $True -IPv6Enabled $True -V1IPv4Enabled $True

@echo [34mRDMA can increase networking throughput, reduce latency, and reduce processor utilization.[0m & @echo.
powershell.exe Enable-NetAdapterRdma -Name * -IncludeHidden
powershell.exe Set-NetAdapterRdma -Name * -IncludeHidden -Enabled $True

@echo [34menable security mpp and security profiles.[0m & @echo.
netsh int tcp set security mpp=enable
netsh int tcp set security profiles=enable

@echo. & @echo [34mSetting MTU to 1492 PPPoE - Ethernet II MTU (1500) less PPPoE header (8). Big MTU has some downsides if the network transmission is not so stable.[0m
powershell.exe New-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters -Name MTU -PropertyType dword -Value 1492 -force
powershell.exe "Get-Item -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces\*"|New-ItemProperty -Name MTU -PropertyType dword -Value 1492 -force" 
powershell.exe "Get-Item -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip6\Parameters\Interfaces\*"|New-ItemProperty -Name MTU -PropertyType dword -Value 1492 -force"
powershell.exe "Get-Item -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Netbt\Parameters\Interfaces\*"|New-ItemProperty -Name MTU -PropertyType dword -Value 1492 -force"
powershell.exe "Get-Item -Path "HKLM:\SYSTEM\CurrentControlSet\Services\AFD\Parameters"|New-ItemProperty -Name FastSendDatagramThreshold -PropertyType dword -Value 1492 -force"
powershell.exe New-Item -Path 'HKLM:\SOFTWARE\Microsoft' -Name 'MSMQ' -ErrorAction SilentlyContinue >nul >nul
powershell.exe New-Item -Path 'HKLM:\SOFTWARE\Microsoft\MSMQ' -Name 'Parameters' -ErrorAction SilentlyContinue >nul >nul
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\MSMQ\Parameters' -Name MTU -PropertyType dword -Value 1492 -force

@echo  [34mBecause the removal of node splitting can potentially impact existing applications, a registry value is available to allow
@echo opting back into the legacy node splitting behavior. Node splitting can be re-enabled by creating a REG_DWORD value
@echo named "SplitLargeNodes" with value 1 underneath.[0m & @echo.
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\NUMA' -Name 'SplitLargeNodes' -PropertyType dword -Value 1 -force

@echo [34mCreating Psched property to define the wide band (%) for system.[0m & @echo.
powershell.exe New-Item -Path 'HKLM:\Software\Policies\Microsoft\Windows' -Name 'Psched' -ErrorAction SilentlyContinue >nul
@echo [34mDefining the wide band (5%) for system.[0m & @echo.
powershell.exe New-ItemProperty -Path 'HKLM:\Software\Policies\Microsoft\Windows\Psched' -Name 'NonBestEffortLimit' -PropertyType dword -Value 5 -force

@echo [34mIncreasing peding package to 196605. Default 65535. Not define in system.[0m & @echo.
powershell.exe New-ItemProperty -Path 'HKLM:\Software\Policies\Microsoft\Windows\Psched' -Name 'MaxOutstandingSends' -PropertyType dword -Value 196605 -force

@echo [34mSet Max User Port to start=1024 num=64512[0m & @echo.
netsh int ipv4 set dynamicport tcp start=1024 num=64512

@echo [34mNetwork direct memory acess ON. Not work together with Chimney Offload. Is the same as netsh int tcp set global netdma.[0m & @echo.
powershell.exe New-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters -Name EnableTCPA -PropertyType dword -Value 1 -force

@echo [34mSetting TTL to 60. If you have frequent problems with packets expiring too quickly, you can set the TTL to a higher value. DefaultTTL 128.[0m & @echo.
rem  In TCP IP networks, any information travels through packets. The TTL is the number of hops between devices (routers and others) that a packet can take before
rem reaching its destination.
rem  The maximum value for the TTL of a packet is 255. Each packet sent to a network is from the sender with a given TTL.
rem On each device that a network packet passes through, the TTL of this packet is decreased by 1. When the TTL reaches zero, the packet is discarded,
rem and stop traveling over the network. The purpose of using a TTL is to avoid that a packet is infinitely wandering through the network, 
rem which would lead to performance problems in the medium and long term.
powershell.exe new-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters -Name DefaultTTL -PropertyType dword -Value 60 -force
powershell.exe "Get-Item -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces\*"|New-ItemProperty -Name DefaultTTL -PropertyType dword -Value 60 -force"
powershell.exe "Get-Item -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip6\Parameters\Interfaces\*"|New-ItemProperty -Name DefaultTTL -PropertyType dword -Value 60 -force"
powershell.exe "Get-Item -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Netbt\Parameters\Interfaces\*"|New-ItemProperty -Name DefaultTTL -PropertyType dword -Value 60 -force"

@echo [34mDisable TCP selective acks option for better CPU utilization.[34m & @echo.
powershell.exe new-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" -Name 'SackOpts' -PropertyType dword -Value 0 -force

@echo [34mTcp1323pts set to 1 - window scaling enabled.[0m & @echo.
rem Value	Meaning
rem 0 	Timestamps and window scaling are disabled.
rem 1   Window scaling is enabled.
rem 2   Timestamps are enabled.
rem 3   Timestamps and window scaling are enabled.
powershell.exe new-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters -Name Tcp1323Opts -PropertyType dword -Value 1 -force

@echo  [34mThis NDIS 5 setting allows for reducing CPU load by offloading some tasks required to maintain the TCP/IP stack to the network card.[0m & @echo.
powershell.exe New-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters -Name DisableTaskOffload -PropertyType dword -Value 0 -force

@echo  [34mIf you set this parameter to 1 (True), TCP tries to detect "Black Hole" routers while doing Path MTU Discovery.[0m & @echo.
powershell.exe New-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters -Name EnablePMTUBHDetect -PropertyType dword -Value 1 -force

rem @echo  [34mIf you set this parameter to 1 (True), TCP tries to discover the Maximum Transmission Unit (MTU or largest packet size) over the path to a remote host.[0m & @echo.
rem powershell.exe New-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters -Name EnablePMTUDiscovery -PropertyType dword -Value 1 -force

@echo [34mIf you set this parameter to 1, TCP uses the Dead Gateway Detection feature.[0m & @echo.
powershell.exe New-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters -Name EnableDeadGWDetect -PropertyType dword -Value 1 -force

@echo [34mDisable large MTU. Big MTU has some downsides if the network transmission is not so stable.[0m & @echo.
powershell.exe New-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters -Name DisableLargeMTU -PropertyType dword -Value 1 -force

@echo [34mThis parameter determines the number of times that TCP retransmits a connect request (SYN) before aborting the attempt. Set to 3.[0m & @echo.
powershell.exe New-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters -Name TcpMaxConnectRetransmissions -PropertyType dword -Value 3 -force

@echo [34mThis parameter controls the number of times that TCP retransmits an individual data segment (non-connect segment) before it aborts the connection.Default 5. Set to 3.[0m & @echo.
powershell.exe New-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters -Name TCPMaxDataRetransmissions -PropertyType dword -Value 3 -force

@echo  [34mEnable Sync attack protection.[0m & @echo.
powershell.exe New-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters -Name SynAttackProtect -PropertyType dword -Value 1 -force

@echo [34mDisable connection rate limiting.[0m & @echo.
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters' -Name 'EnableConnectionRateLimiting' -PropertyType dword -Value '0' -force

@echo [34mEnables direct cache acess.[0m & @echo.
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters' -Name 'EnableDca' -PropertyType dword -Value '1' -force

@echo [34mSecurity setting. Requires Network Level Authentication (NLA).[0m & @echo. 
powershell.exe New-Item -Path 'HKLM:\System\CurrentControlSet\Services\Tcpip' -Name 'QoS' -ErrorAction SilentlyContinue >nul
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\services\Tcpip\QoS' -Name 'Do not use NLA' -PropertyType string -Value 0 -force

rem IRPStackSize
rem 4) Assign recommended value: 32
rem Default value(when not present in registry): 15
rem Possible range: 1-50
rem Possible issues: 33+
@echo [34mLanmanWorkstation. Setting IRP Stack Size to 33.[0m & @echo.
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Services\LanmanWorkstation\Parameters' -Name 'IRPStackSize' -PropertyType dword -Value 33 -force

@echo [34mLanmanWorkstation. Setting Minimum Free Connection to 128.[0m
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Services\LanmanWorkstation\Parameters' -Name 'MinFreeConnections' -PropertyType dword -Value 128 -force

@echo [34mLanmanWorkstation. Security setting. Require Security Signature.[0m
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Services\LanmanWorkstation\Parameters' -Name 'RequireSecuritySignature' -PropertyType dword -Value 1 -force

@echo [34mLanmanServer. Setting IRP Stack Size to 33.[0m & @echo.
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters' -Name 'IRPStackSize' -PropertyType dword -Value 33 -force

@echo [34mLanmanServer. Setting Minimum Free Connection to 128.[0m
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters' -Name 'MinFreeConnections' -PropertyType dword -Value 128 -force

@echo [34mLanmanServer. Security setting. Require Security Signature.[0m
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters' -Name 'RequireSecuritySignature' -PropertyType dword -Value 1 -force

@echo [34mDetermines the time that must elapse before TCP/IP can release a closed connection and reuse its resources. Setting to 28[0m & @echo.
rem This parameter applies only to the Windows® operating system. It determines the time that must elapse before TCP can release a closed connection and reuse its resources.
rem The value for Max Connections is 100.
rem The value for Min Connections is 10.
rem The recommended value is 30.
rem Testing at 28.
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters' -Name 'TcpTimedWaitDelay' -PropertyType dword -Value '28' -force

@echo [34mThis parameter limits the maximum number of connections that TCP can have open at the same time. Setting to 65534.[0m
powershell.exe New-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters -Name 'TcpNumConnections' -PropertyType dword -Value 65534 -force

@echo  [34mIt determines how many active TCP connections your computer can handle at any given time based on how much physical memory
@echo you have and how much performance your computer has with regard to bandwidth. Max value is 65536.  (set to 1/4 of max value).[0m & @echo.
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters' -Name MaxFreeTcbs -PropertyType dword -Value 46811 -force

@echo [34mSetting DNS and Hosts Priority.[0m & @echo.
powershell.exe New-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\ServiceProvider -Name Class -PropertyType dword -Value 2 -force
powershell.exe New-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\ServiceProvider -Name LocalPriority -PropertyType dword -Value 4 -force
powershell.exe New-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\ServiceProvider -Name DnsPriority -PropertyType dword -Value 5 -force
powershell.exe New-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\ServiceProvider -Name HostsPriority -PropertyType dword -Value 6 -force
powershell.exe New-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\ServiceProvider -Name NetbtPriority -PropertyType dword -Value 7 -force

@echo  [34mStart with CPU1 for RSS (Receive Side Scaling Base set to value of 1) to let CPU0 do other important things.[0m & @echo.
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\services\NDIS\Parameters' -Name 'RssBaseCpu' -PropertyType dword -Value '1' -force

@echo [34mSet the maximum number of RSS CPUs with the MaxNumRssCpus. DUO CORE set value of 2.[0m & @echo.
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\services\NDIS\Parameters' -Name 'MaxNumRssCpus' -PropertyType dword -Value '2' -force

@echo [34mThe AllowFlowControlUnderDebugger registry value prevents NDIS from disabling flow control, and allows NICs to keep their configured behavior.[0m & @echo.
powershell.exe New-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\services\NDIS\Parameters -Name 'AllowFlowControlUnderDebugger' -PropertyType dword -Value 1 -force

@echo [34mProcessorAffinityMask. Specifies which processors can be associated with a network adapter and service the delayed procedure calls (DPCs) generated by that network adapter. 
@echo This entry is designed for multiprocessor computers, specifically those with more than one network adapter. 
@echo Value set to 0, none of the processors are associated with network adapters. DPCs are serviced by the same processor that serviced the interrupt.[0m & @echo.
REM Value	Meaning
REM 0x0	If the value of this entry is 0 (all bits are set to 0), none of the processors are associated with network adapters. DPCs are serviced by the same processor that serviced the interrupt. 
REM This setting is useful for platforms that distribute interrupts among all processors, such as the Windows 2000 and Windows NT 4.0 platforms for Intel Pentium and Pentium Pro (P6) processors.
REM 0x1 - 0xFFFFFFFE (DEC 4294967294)	If some of the bits are set to 0 and others are set to 1, the system skips processors associated with bits set to 0 and assigns network adapters to processors whose bits are set to 1.
REM 0xFFFFFFFF (DEC 4294967295)	If the value of this entry is 0xFFFFFFFF (all bits are set to 1), all processors on the computer can be associated with network adapters. 
REM If there are multiple processors and multiple network adapters, each adapter is associated with one processor and services all of its DPCs.
REM The first adapter is associated with the processor with the highest number. Subsequent adapters are associated with the next processor in descending numeric order.
REM If there are more adapters than there are processors, the system begins again at the highest numbered processor and assigns a network adapter to each remaining processor in descending numeric order.
powershell.exe New-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\services\NDIS\Parameters -Name ProcessorAffinityMask -PropertyType dword -Value 0 -force

@echo [34mSetting NetworkThrottlingIndex to max for better gamming experience.[0m  & @echo.
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile' -Name NetworkThrottlingIndex -PropertyType dword -Value 4294967295 -force

@echo [34mSystem Responsiveness determines the percentage of CPU resources that should be guaranteed to low-priority tasks.
@echo Note that values that are not evenly divisible by 10 are rounded up to the nearest multiple of 10. A value of 0 is also treated as 10. Setting to 0[0m & @echo.
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile' -Name 'SystemResponsiveness' -PropertyType dword -Value 0 -force


@echo [34mGaming Tweaks.[0m & @echo.
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games' -Name Affinity -PropertyType dword -Value 0 -force
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games' -Name 'Background Only' -PropertyType string -Value False -force
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games' -Name Priority -PropertyType dword -Value 2 -force
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games' -Name 'Scheduling Category' -PropertyType string -Value High -force
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games' -Name 'SFIO Priority' -PropertyType string -Value High -force
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games' -Name 'Latency Sensitive' -PropertyType string -Value True -force
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games' -Name NetworkThrottling -PropertyType dword -Value 4294967295 -force
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games' -Name 'Clock Rate' -PropertyType dword -Value 10000 -force
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games' -Name 'GPU Priority' -PropertyType dword -Value 8 -force

powershell.exe New-Item -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks' -Name 'Low Latency' -ErrorAction SilentlyContinue >nul
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Low Latency' -Name Affinity -PropertyType dword -Value 0 -force
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Low Latency' -Name 'Background Only' -PropertyType string -Value False -force
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Low Latency' -Name 'Priority' -PropertyType dword -Value 2 -force
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Low Latency' -Name 'Scheduling Category' -PropertyType string -Value High -force
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Low Latency' -Name 'SFIO Priority' -PropertyType string -Value Normal -force
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Low Latency' -Name 'Latency Sensitive' -PropertyType string -Value True -force
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Low Latency' -Name NetworkThrottling -PropertyType dword -Value 4294967295 -force
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Low Latency' -Name 'Clock Rate' -PropertyType dword -Value 10000 -force
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Low Latency' -Name 'GPU Priority' -PropertyType dword -Value 8 -force


powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Audio' -Name Affinity -PropertyType dword -Value 0 -force
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Audio' -Name 'Background Only' -PropertyType string -Value False -force
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Audio' -Name Priority -PropertyType dword -Value 5 -force
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Audio' -Name 'Scheduling Category' -PropertyType string -Value medium -force
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Audio' -Name 'SFIO Priority' -PropertyType string -Value Normal -force
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Audio' -Name 'Latency Sensitive' -PropertyType string -Value True -force
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Audio' -Name NetworkThrottling -PropertyType dword -Value 4294967295 -force
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Audio' -Name 'Clock Rate' -PropertyType dword -Value 10000 -force
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Audio' -Name 'GPU Priority' -PropertyType dword -Value 8 -force

powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Pro Audio' -Name Affinity -PropertyType dword -Value 0 -force
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Pro Audio' -Name 'Background Only' -PropertyType string -Value False -force
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Pro Audio' -Name Priority -PropertyType dword -Value 6 -force
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Pro Audio' -Name 'Scheduling Category' -PropertyType string -Value medium -force
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Pro Audio' -Name 'SFIO Priority' -PropertyType string -Value Normal -force
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Pro Audio' -Name 'Latency Sensitive' -PropertyType string -Value True -force
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Pro Audio' -Name NetworkThrottling -PropertyType dword -Value 4294967295 -force
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Pro Audio' -Name 'Clock Rate' -PropertyType dword -Value 10000 -force
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Pro Audio' -Name 'GPU Priority' -PropertyType dword -Value 8 -force

@echo [34mtweaking video propertys.[0m & @echo.
@echo [47m[31mIgnore red info in this tweak, is write protected regestry![0m
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Video\*\*' 'PP_ThermalAutoThrottlingEnable' -PropertyType dword -Value 0 -force
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Video\*\*' 'DalAllowDirectMemoryAccessTrig' -PropertyType dword -Value 1 -force
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Video\*\*' 'DedicatedSegmentSize' -PropertyType dword -Value 8192 -force
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Video\*\*' 'DalAllowDirectMemoryAccessTrig' -PropertyType dword -Value 1 -force
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Video\*\*' 'PruningMode' -PropertyType dword -Value 0 -force
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Video\*\*' 'MultiFunctionSupported' -PropertyType dword -Value 1 -force
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Video\*\*' 'AllowSubscription' -PropertyType dword -Value 0 -force
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Video\*\*' 'KMD_DeLagEnabled' -PropertyType dword -Value 1 -force
rem powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Video\*\*' 'VgaCompatible' -PropertyType dword -Value 1 -force
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Video\*\*' 'MosquitoNoiseRemoval_NA' -PropertyType string -Value 1 -force

@echo [34mDisabling Nagle´s Algorithm.[0m& @echo.
powershell.exe "Get-Item -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces\*"|New-ItemProperty -Name 'TcpDelAckTicks' -PropertyType dword -Value 0 -force"
powershell.exe "Get-Item -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces\*"|New-ItemProperty -Name 'TCPAckFrequency' -PropertyType dword -Value 1 -force"
powershell.exe "Get-Item -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces\*"|New-ItemProperty -Name 'TCPNoDelay' -PropertyType dword -Value 1 -force"
powershell.exe "Get-Item -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip6\Parameters\Interfaces\*"|New-ItemProperty -Name 'TcpDelAckTicks' -PropertyType dword -Value 0 -force"
powershell.exe "Get-Item -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip6\Parameters\Interfaces\*"|New-ItemProperty -Name 'TCPAckFrequency' -PropertyType dword -Value 1 -force"
powershell.exe "Get-Item -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip6\Parameters\Interfaces\*"|New-ItemProperty -Name 'TCPNoDelay' -PropertyType dword -Value 1 -force"
powershell.exe "Get-Item -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Netbt\Parameters\Interfaces\*"|New-ItemProperty -Name 'TcpDelAckTicks' -PropertyType dword -Value 0 -force"
powershell.exe "Get-Item -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Netbt\Parameters\Interfaces\*"|New-ItemProperty -Name 'TCPAckFrequency' -PropertyType dword -Value 1 -force"
powershell.exe "Get-Item -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Netbt\Parameters\Interfaces\*"|New-ItemProperty -Name 'TCPNoDelay' -PropertyType dword -Value 1 -force"

@echo [34mSetting DNS.[0m & @echo.
@echo  [1m[36mCloudFlare[0m
@echo  [33mFree DNS.[0m
@echo  IPV4 DNS1 1.1.1.1
@echo  IPV4 DNS2 1.0.0.1
@echo  IPV6 DNS1 2606:4700:4700::1111
@echo  IPV6 DNS2 2606:4700:4700::1001 & @echo.
@echo  [33mMalware blocking only.[0m
@echo  IPV4 DNS1 1.1.1.2
@echo  IPV4 DNS2 1.0.0.2
@echo  IPV6 DNS1 2606:4700:4700::1112
@echo  IPV6 DNS2 2606:4700:4700::1002 & @echo.
@echo  [33mMalware and adult content blocking.[0m
@echo  IPV4 DNS1 1.1.1.3
@echo  IPV4 DNS2 1.0.0.3
@echo  IPV6 DNS1 2606:4700:4700::1113
@echo  IPV6 DNS2 2606:4700:4700::1003
@echo. & @echo. & @echo.
@echo  [1m[36mGoogle[0m
@echo  [33mFree DnsPriority.[0m
@echo  IPV4 DNS1 8.8.8.8
@echo  IPV4 DNS2 8.8.4.4
@echo  IPV6 DNS1 2001:4860:4860::8888
@echo  IPV6 DNS2 2001:4860:4860::8844
@echo. & @echo. & @echo.
@echo  [1m[36mNorton[0m
@echo  [33mFree DNS malware and phishing blocking only.[0m
@echo  IPV4 DNS1 199.85.126.10
@echo  IPV4 DNS2 199.85.127.10
@echo  IPV6 DNS1 ****
@echo  IPV6 DNS2 **** & @echo.
@echo  [33mFree DNS malware, phishing and Porn blocking only.[0m
@echo  IPV4 DNS1 199.85.126.20
@echo  IPV4 DNS2 199.85.127.20
@echo  IPV6 DNS1 ****
@echo  IPV6 DNS2 **** & @echo.
@echo  [33mFree DNS malware, phishing,alcool, Porn drugs and others blocking.[0m
@echo  IPV4 DNS1 199.85.126.30
@echo  IPV4 DNS2 199.85.127.30
@echo  IPV6 DNS1 ****
@echo  IPV6 DNS2 **** & @echo.
@echo  [1m[36mQuad9 Free DNS[0m
@echo  [33mMalware Blocking, DNSSEC Validation (this is the most typical configuration)[0m
@echo  IPV4 DNS1 9.9.9.9
@echo  IPV4 DNS2 149.112.112.112
@echo  IPV6 DNS1 2620:fe::fe
@echo  IPV6 DNS2 2620:fe::9 & @echo.
@echo  [33mSecured w/ECS: Malware blocking, DNSSEC Validation, ECS enabled[0m
@echo  IPV4 DNS1 9.9.9.11
@echo  IPV4 DNS2 149.112.112.11
@echo  IPV6 DNS1 2620:fe::11
@echo  IPV6 DNS2 2620:fe::fe:11 & @echo.
@echo  [1m[31m=NOT RECOMENDED= Unsecured:[0m [33m No Malware blocking, no DNSSEC validation (for experts only!)[0m
@echo  IPV4 DNS1 9.9.9.10
@echo  IPV4 DNS2 149.112.112.10
@echo  IPV6 DNS1 2620:fe::10
@echo  IPV6 DNS2 2620:fe::fe:10 & @echo.
@echo. & @echo. [46m[30m
Set /p DNS="-Copy/Paste here IPV4 DNS1 value to set: "
Set /p DNS2="-Copy/Paste here IPV4 DNS2 value to set: "
Set /p IPV6DNS="-Copy/Paste here IPV6 DNS1 value to set: "
Set /p IPV6DNS2="-Copy/Paste here IPV6 DNS2 value to set: "
@echo. [0m
@echo [37mSetting Interface to DNS %DNS% and %DNS2% & @echo.
@echo [37mSetting Interface to IPV6 DNS %IPV6DNS% and %IPV6DNS2% & @echo. & @echo.[33m
powershell.exe "Get-Item -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces\*"|New-ItemProperty -Name 'NameServer' -PropertyType String -Value '%DNS%,%DNS2%' -force
powershell.exe "Get-Item -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip6\Parameters\Interfaces\*"|New-ItemProperty -Name 'NameServer' -PropertyType String -Value '%IPV6DNS%,%IPV6DNS2%' -force
powershell.exe "Get-Item -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Netbt\Parameters\Interfaces\*"|New-ItemProperty -Name 'NameServer' -PropertyType String -Value '%DNS%,%DNS2%' -force
@echo. & @echo [1m[32mDone![0m & @echo.

@echo  [32mSet your Metric value.[0m & @echo.
@echo  [47m[31m Download Speed[0m	                                                  [47m[31mMetric[0m
@echo  [33mGreater than or equal to 2 GB	                                             5[0m
@echo  Greater than 200 Mb	                                                    10
@echo  [33mGreater than 20 Mb, and less than or equal to 200 Mb             	    20[0m
@echo  Greater than 4 Mb, and less than or equal to 20 Mb	                    30
@echo  [33mGreater than 500 kilobits (Kb), and less than or equal to 4 Mb	            40[0m
@echo  Less than or equal to 500 Kb	                                            50 & @echo.
@echo. [46m[30m
Set /p MET="-Insert here the metric value to set: "
@echo. [0m
@echo [37mSetting Interface metric to %MET%.[0m & @echo.
powershell.exe "Get-Item -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces\*"|New-ItemProperty -Name InterfaceMetric -PropertyType dword -Value %MET% -force" > nul 
powershell.exe "Get-Item -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip6\Parameters\Interfaces\*"|New-ItemProperty -Name InterfaceMetric -PropertyType dword -Value %MET% -force" > nul 
powershell.exe "Get-Item -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Netbt\Parameters\Interfaces\*"|New-ItemProperty -Name InterfaceMetric -PropertyType dword -Value %MET% -force" > nul 
@echo.

@echo [34mBetter IO performance.[0m & @echo.
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\kernel' -Name 'MaximumDpcQueueDepth' -PropertyType dword -Value 1 -force

@echo [34mTurn On reptoline.[0m & @echo.
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management' -Name FeatureSettingsOverride -PropertyType dword -Value 1024 -force
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management' -Name FeatureSettingsOverrideMask -PropertyType dword -Value 1024 -force

@echo [34mDisable Prefetch in Windows 11/10 for better SSD performance.[0m & @echo.
rem 0 – Disable SysMain
rem 1 – Enable SysMain for boot files only
rem 2 – Enable SysMain for applications only
rem 3 – Enable SysMain for both boot files and applications
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management\PrefetchParameters' -Name 'EnablePrefetcher' -PropertyType dword -Value 0 -force

@echo [34mEnable Trim on SSD.[0m & @echo.
fsutil behavior set DisableDeleteNotify 0 >nul
fsutil behavior set DisableDeleteNotify NTFS 0 >nul
fsutil behavior set DisableDeleteNotify ReFS 0 >nul

rem 80000000 (hex)= 2147483648 (Dec) = User Managed, Last Access Updates Enabled
rem 80000001 (hex)= 2147483649 (Dec) = User Managed, Last Access Updates Disabled
rem 80000002 (hex)= 2147483650 (Dec) = System Managed, Last Access Updates Enabled
rem 80000003 (hex)= 2147483651 (Dec) = System Managed, Last Access Updates Disabled
@echo [34mImproving NTFS Performance, System Managed, Last Access Updates Disabled.[0m & @echo. 
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem' -Name 'NtfsDisableLastAccessUpdate' -PropertyType dword -Value '2147483651' -force

@echo [34mCreating missing folders TileDataLayer and Database.[0m & @echo.
mkdir  "%systemroot%\system32\config\systemprofile\AppData\Local\TileDataLayer" >nul
mkdir  "%systemroot%\system32\config\systemprofile\AppData\Local\TileDataLayer\Database" >nul

@echo [34mEnabling Storage Management Cache.[0m & @echo.
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\StorageManagement\SpacesSMP\ConnectedSubsystems\*' -Name 'CacheEnabled' -PropertyType dword -Value 1 -force 

@echo [34mEnabling Memory Management Third Level Data Cache.[0m & @echo.
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management' -Name 'ThirdLevelDataCache' -PropertyType dword -Value 0 -force

@echo [34mMaximizes the size of the virtual address space used for the paged pool to 0. The system algorithm typically sets the size of the paged pool to slightly less than the amount of physical memory in the computer. This value is optimal for most systems.[0m & @echo.
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management' -Name 'PagedPoolSize' -PropertyType dword -Value 0 -force

@echo [34mSetting SystemPages to 0.[0m & @echo.
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management' -Name 'SystemPages' -PropertyType dword -Value 0 -force

@echo [34mTurn on automatic driver searching.[0m & @echo.
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\DriverSearching' -Name 'SearchOrderConfig' -PropertyType dword -Value 1 -force

@echo [34mDisabling Windows Fast boot feature. Disabling Fast Startup slows Boot but will improves is performance.[0m & @echo.
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Power' -Name 'HiberBootEnabled' -PropertyType dword -Value 0 -force

@echo [34mPreventing computer from pushing other apps including the background apps into the suppressed state and triggers high performance.[0m & @echo.
powershell.exe New-Item -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Power' -Name 'PowerThrottling' -force -ErrorAction SilentlyContinue >nul
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Power\PowerThrottling' -Name 'PowerThrottlingOff' -PropertyType dword -Value 1 -force

@echo [34mDisable the Game DVR system that often interferes with the actual game. If you use Game DVR, set value to 1.[0m & @echo.
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\PolicyManager\default\ApplicationManagement\AllowGameDVR' -Name 'Value' -PropertyType dword -Value 0 -force

@echo [34mDisable the 'intelppm" service, fix the "CPU Not Running at Full Speed" issue, is to prevent the "intelppm" service to start, using registry.
@echo Modify the value data to '4' ( always at full speed)
@echo Modify the value data to '1' ( use full speed only when need it).[0m & @echo.
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Services\intelppm' -Name 'Start'  -PropertyType dword -Value 2 -force
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Services\intelpmax' -Name 'Start'  -PropertyType dword -Value 2 -force

@echo [34mUnlock additional Windows power plan settings.[0m & @echo.
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Power' -Name 'CsEnabled'  -PropertyType dword -Value 1 -force

@echo [34mNtfsMemoryUsage - When set to 2, NTFS increases the size of its lookaside lists and memory thresholds.[0m & @echo.
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem' -Name 'NtfsMemoryUsage'  -PropertyType dword -Value 2 -force

@echo [34mSet Class 1Initial Unpark Count to 33. Default value 16.[0m & @echo.
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Power' -Name 'Class1InitialUnparkCount'  -PropertyType dword -Value 33 -force

@echo  [34mIncrease the heap size to improve performance.
@echo  The value xxxx defines the maximum size of the system-wide heap (in kilobytes), yyyy defines the size of each desktop heap,
@echo and zzzz defines the size of the desktop heap that is associated with a non-interactive Windows station.[0m & @echo.
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\SubSystems' -Name 'SharedSection'  -PropertyType string -Value '2048,3072,2048' -force

@echo [34mIncrease Performance for Programs, read Note.[0m & @echo.
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\PriorityControl' -Name 'Win32PrioritySeparation'  -PropertyType dword -Value 38 -force

@echo [34mHardware Accelerated GPU Scheduling enable.[0m & @echo.
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\GraphicsDrivers' -Name 'HwSchMode'  -PropertyType dword -Value 2 -force

@echo [34mTurning Off all windows suggestions.[0m & @echo.
powershell.exe New-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager' -Name 'ContentDeliveryAllowed' -PropertyType dword -Value 0 -force
powershell.exe New-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager' -Name 'SubscribedContent-310093Enabled' -PropertyType dword -Value 0 -force
powershell.exe New-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager' -Name 'SubscribedContent-338388Enabled' -PropertyType dword -Value 0 -force
powershell.exe New-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager' -Name 'SubscribedContent-338389Enabled' -PropertyType dword -Value 0 -force
powershell.exe New-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager' -Name 'SubscribedContent-88000326Enabled' -PropertyType dword -Value 0 -force
powershell.exe New-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager' -Name 'SilentInstalledAppsEnabled' -PropertyType dword -Value 0 -force
powershell.exe New-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager' -Name 'SystemPaneSuggestionsEnabled' -PropertyType dword -Value 0 -force

@echo [34mTurn off auto reboot after crash.[0m & @echo.
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\CrashControl' -Name 'AutoReboot' -PropertyType dword -Value 0 -force  

@echo [34mEnabling Windows Educational Themes.[0m & @echo.
powershell.exe New-Item -Path 'HKLM:\SOFTWARE\Microsoft\PolicyManager\current\device' -Name 'Education' -ErrorAction SilentlyContinue >nul
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\PolicyManager\current\device\Education' -Name 'EnableEduThemes' -PropertyType dword -Value 1 -force

@echo [34mEnabling Windows Stickers.[0m & @echo.
powershell.exe New-Item -Path 'HKLM:\SOFTWARE\Microsoft\PolicyManager\current\device' -Name 'Stickers' -ErrorAction SilentlyContinue >nul
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\PolicyManager\current\device\Stickers' -Name 'EnableStickers' -PropertyType dword -Value 1 -force

@echo [34mComposition DWM Tweaks.[0m
powershell.exe New-ItemProperty -Path 'HKCU:\SOFTWARE\Microsoft\Windows\Dwm' -Name 'DisableHologramCompositor' -PropertyType dword -Value 0 -force
powershell.exe New-ItemProperty -Path 'HKCU:\SOFTWARE\Microsoft\Windows\Dwm' -Name 'EnableAeroPeek' -PropertyType dword -Value 1 -force
powershell.exe New-ItemProperty -Path 'HKCU:\SOFTWARE\Microsoft\Windows\Dwm' -Name 'ColorPrevalence' -PropertyType dword -Value 1 -force
powershell.exe New-ItemProperty -Path 'HKCU:\SOFTWARE\Microsoft\Windows\Dwm' -Name 'EnableWindowColorization' -PropertyType dword -Value 1 -force
powershell.exe New-ItemProperty -Path 'HKCU:\SOFTWARE\Microsoft\Windows\Dwm' -Name 'ForceEffectMode' -PropertyType dword -Value 1 -force
powershell.exe New-ItemProperty -Path 'HKCU:\SOFTWARE\Microsoft\Windows\Dwm' -Name 'MaxD3DFeatureLevel' -PropertyType dword -Value 64 -force
powershell.exe New-ItemProperty -Path 'HKCU:\SOFTWARE\Microsoft\Windows\Dwm' -Name 'OneCoreNoDWMRawGameController' -PropertyType dword -Value 1 -force

@echo [34mSetting Dark mode Theme.[0m
powershell.exe New-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize' -Name 'AppsUseLightTheme' -PropertyType dword -Value 0 -force
powershell.exe New-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize' -Name 'SystemUsesLightTheme' -PropertyType dword -Value 0 -force
powershell.exe New-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize' -Name 'ColorPrevalence' -PropertyType dword -Value 0 -force
powershell.exe New-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize' -Name 'EnableTransparency' -PropertyType dword -Value 1 -force
powershell.exe New-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Themes\History' -Name 'AutoColor' -PropertyType dword -Value 0 -force

@echo [34mImport wallpaper at 95%.[0m
powershell.exe New-ItemProperty -Path 'HKCU:\Control Panel\Desktop' -Name 'JPEGImportQuality' -PropertyType dword -Value 95 -force

@echo [34mFGBoost Decay. This feature can be disabled for debugging or isolating performance related problems.[0m & @echo.
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\KernelVelocity' -Name 'DisableFGBoostDecay' -PropertyType dword -Value 0 -force

@echo [34mTurn off Lazy mode.[0m & @echo.
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile' -Name 'NoLazyMode' -PropertyType dword -Value 1 -force

@echo [34mEnabling NV Cache.[0m & @echo.
powershell.exe New-Item -Path 'HKLM:\Software\Policies\Microsoft\Windows' -Name 'NvCache' -ErrorAction SilentlyContinue >nul
powershell.exe New-ItemProperty -Path 'HKLM:\Software\Policies\Microsoft\Windows\NvCache' -Name 'EnableNvCache' -PropertyType dword -Value 1 -force

@echo [34mDisabling Solid State Mode. Works better on SSDs.[0m & @echo.
powershell.exe New-ItemProperty -Path 'HKLM:\Software\Policies\Microsoft\Windows\NvCache' -Name 'EnableSolidStateMode' -PropertyType dword -Value 0 -force

@echo [34mMicrosoft Edge, enable compatibility mode.[0m & @echo.
powershell.exe New-Item -Path 'HKLM:\Software\Policies\Microsoft' -Name 'MicrosoftEdge' -ErrorAction SilentlyContinue >nul
powershell.exe New-Item -Path 'HKLM:\Software\Policies\Microsoft\MicrosoftEdge' -Name 'BrowserEmulation' -ErrorAction SilentlyContinue >nul
powershell.exe New-ItemProperty -Path 'HKLM:\Software\Policies\Microsoft\MicrosoftEdge\BrowserEmulation' -Name 'MSCompatibilityMode' -PropertyType dword -Value 1 -force

@echo [34mPrevent Edge pre-launching.[0m & @echo.
powershell.exe New-Item -Path 'HKLM:\Software\Policies\Microsoft\MicrosoftEdge' -Name 'Main' -ErrorAction SilentlyContinue >nul
powershell.exe New-ItemProperty -Path 'HKLM:\Software\Policies\Microsoft\MicrosoftEdge\Main' -Name 'AllowPrelaunch' -PropertyType dword -Value 0 -force

@echo [34mPrevent Chrome pre-launching.[0m & @echo.
powershell.exe New-Item -Path 'HKLM:\SOFTWARE\Google\Chrome' -Name 'Main' -ErrorAction SilentlyContinue >nul
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Google\Chrome\Main' -Name 'AllowPrelaunch' -PropertyType dword -Value 0 -force

@echo [34mChrome, enable compatibility mode.[0m & @echo.
powershell.exe New-Item -Path 'HKLM:\SOFTWARE\Google\Chrome' -Name 'BrowserEmulation' -ErrorAction SilentlyContinue >nul
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Google\Chrome\BrowserEmulation' -Name 'MSCompatibilityMode' -PropertyType dword -Value 1 -force

@echo Download missing COM components. & @echo.
powershell.exe New-Item -Path 'HKLM:\Software\Policies\Microsoft\Windows' -Name 'App Management' -ErrorAction SilentlyContinue >nul
powershell.exe New-ItemProperty -Path 'HKLM:\Software\Policies\Microsoft\Windows\App Management' -Name 'COMClassStore' -PropertyType dword -Value 1 -force

@echo [34mDisabling Window Scaling Heuristics State.[0m & @echo.
powershell.exe New-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Services\Tcpip\Parameters' -Name 'EnableWsd' -PropertyType dword -Value 0 -force

@echo [34mMinimizing the number of simultaneous connections to the Internet on Windows Domain: Don´t allow simultaneous connections.[0m & @echo.
powershell.exe New-ItemProperty -Path 'HKLM:\Software\Policies\Microsoft\Windows\WcmSvc\GroupPolicy' -Name 'fMinimizeConnections' -PropertyType dword -Value 1 -force


rem - 1 - Unrestricted: Use of this connection is unlimited and not restricted by usage charges and capacity constraints.
rem - 2 - Fixed: Use of this connection is not restricted by usage charges and capacity constraints up to a certain data limit.
rem - 3 - Variable: This connection is costed on a per byte basis.
@echo [34mThis policy setting configures the cost of Wireless LAN (WLAN) connections on the local machine.[0m & @echo.
powershell.exe New-Item -Path 'HKLM:\Software\Policies\Microsoft\Windows' -Name 'Wireless' -ErrorAction SilentlyContinue >nul
powershell.exe New-Item -Path 'HKLM:\Software\Policies\Microsoft\Windows\Wireless' -Name 'NetCost' -ErrorAction SilentlyContinue >nul
powershell.exe New-ItemProperty -Path 'HKLM:\Software\Policies\Microsoft\Windows\Wireless\NetCost' -Name 'Cost' -PropertyType dword -Value 1 -force

@echo [34mThis policy setting configures the cost of Network Connections on the local machine.[0m & @echo.
powershell.exe New-ItemProperty -Path 'HKLM:\Software\Policies\Microsoft\Windows\Network Connections' -Name 'Cost' -PropertyType dword -Value 1 -force

@echo [34mTweaking readyBoost.[0m & @echo.
powershell.exe New-Item -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion' -Name 'EMDMgmt' -ErrorAction SilentlyContinue >nul
powershell.exe New-Item -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\EMDMgmt' -Name '*' -ErrorAction SilentlyContinue >nul
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\EMDMgmt\*' -Name 'DeviceStatus' -PropertyType dword -Value 2 -force
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\EMDMgmt\*' -Name 'WriteSpeedKBs' -PropertyType dword -Value 6144 -force
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\EMDMgmt\*' -Name 'SpeedReadKBs' -PropertyType dword -Value 8192 -force

@echo [34mTurning ON Drivers update on windows update.[0m & @echo.
powershell.exe New-Item -Path 'HKLM:\SOFTWARE\Policies\Microsoft\Windows' -Name 'WindowsUpdate' -ErrorAction SilentlyContinue >nul
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate' -Name 'ExcludeWUDriversInQualityUpdate' -PropertyType dword -Value 0 -force

@echo [34mDisabling defrag for SSD Protection.[0m & @echo.
powershell.exe New-Item -Path 'HKLM:\SOFTWARE\Microsoft\Dfrg' -Name 'BootOptimizeFunction' -ErrorAction SilentlyContinue >nul
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Dfrg\BootOptimizeFunction' -Name 'Enable' -PropertyType string -Value N -force

@echo [34mDisabling Ndu [Network Diagnostic Usage].[0m & @echo.
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Services\Ndu' -Name 'Start' -PropertyType dword -Value 4 -force

@echo [34mAdding and enabling Super Power Scheme.[0m & @echo.
powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61
TIMEOUT -T 2 /nobreak >nul
powercfg -s e9a42b02-d5df-448d-aa00-03f14749eb61

@echo [34mEnabling some visual effects.[0m & @echo.
powershell.exe New-ItemProperty -Path 'HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced' -Name 'TaskbarAnimations' -PropertyType dword -Value '1' -force
powershell.exe New-ItemProperty -Path 'HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects' -Name 'VisualFXSetting' -PropertyType dword -Value '1' -force

@echo [34mShow file extencion[0m
powershell.exe New-ItemProperty -Path 'HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced' -Name 'HideFileExt' -PropertyType dword -Value '0' -force

powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System' -Name 'legalnoticecaption' -PropertyType String -Value 'Windows 11 Pro' -force
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System' -Name 'legalnoticetext' -PropertyType String -Value 'Mod by Persona78' -force

@echo [34mEnabling Auto Game Mode.[0m & @echo.
powershell.exe New-ItemProperty -Path 'HKCU:\SOFTWARE\Microsoft\GameBar' -Name 'AllowAutoGameMode' -PropertyType dword -Value '1' -force
powershell.exe New-ItemProperty -Path 'HKCU:\SOFTWARE\Microsoft\GameBar' -Name 'AutoGameModeEnabled' -PropertyType dword -Value '1' -force

@echo [34mBlock windows background to apps run in background.[0m & @echo.
powershell.exe New-Item -Path 'HKLM:\SOFTWARE\Policies\Microsoft\Windows' -Name 'AppPrivacy' -ErrorAction SilentlyContinue >nul
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Policies\Microsoft\Windows\AppPrivacy' -Name 'LetAppsRunInBackground' -PropertyType dword -Value '0' -force

@echo [34mEnable the audit mode for Lsass.exe on a single computer.[0m
powershell.exe New-Item -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options' -Name 'LSASS.exe' -ErrorAction SilentlyContinue >nul
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\LSASS.exe' -Name 'AuditLevel' -PropertyType dword -Value '8' -force

@echo [34mEnable LSA protection on a single computer.[0m
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Lsa' -Name 'RunAsPPL' -PropertyType dword -Value '2' -force

@echo [34mTweaking Ntfs Parallel Flush Threshold to release RAM earlier.[0m
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem' -Name 'NtfsParallelFlushThreshold' -PropertyType dword -Value 800 -force

@echo [34mEnable Reserved Storage[0m
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\ReserveManager' -Name 'ShippedWithReserves' -PropertyType dword -Value '1' -force


@echo [34mAbsolute Max Cache Size unlimited[0m
powershell.exe New-Item -Path 'HKLM:\SOFTWARE\Policies\Microsoft\Windows' -Name 'DeliveryOptimization' -ErrorAction SilentlyContinue >nul
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Policies\Microsoft\Windows\DeliveryOptimization' -Name 'DOAbsoluteMaxCacheSize' -PropertyType dword -Value '0' -force

@echo [34mFrom 100 Percent define you Bandwith for Background and Foreground aplications.[0m & @echo. [46m[30m
set /p bkground="- From 100, insert Max Percentage Background Bandwidth value here: " & @echo.
set /p FRground="- From 100, insert Max Percentage Foreground Bandwidth value here: " & @echo. [0m

@echo [34mMaximum Background Download Bandwidth (percentage)- set to %bkground%%[0m
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Policies\Microsoft\Windows\DeliveryOptimization' -Name 'DOPercentageMaxBackgroundBandwidth' -PropertyType dword -Value '%bkground%' -force

@echo [34mMaximum Foreground Download Bandwidth (percentage) - set to %FRground%%[0m
powershell.exe New-ItemProperty -Path 'HKLM:\SOFTWARE\Policies\Microsoft\Windows\DeliveryOptimization' -Name 'DOPercentageMaxForegroundBandwidth' -PropertyType dword -Value '%FRground%' -force

@echo [32mCalculating the maximum IoPageLockLimit can lock for I/O operations.[0m & @echo.
@echo. [46m[30m
Set /p value="Write the Max RAM value in system in GB Here: "
@echo. [0m
set /a valueG=%value%*1024
set /a calc=%valueG%*2/16
@echo %calc%
powershell.exe New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management' -Name 'IoPageLockLimit' -PropertyType dword -Value %calc% -force  

@echo. & @echo. & @echo [34mCleanning all system .tmp files. & @echo.
@echo Some files will not be remove because are in use or are protected![0m & @echo.
TIMEOUT -T 3 /nobreak >nul

@echo [1m[32mStart Cleanning tool.[0m
@echo.
for %%a in (%systemdrive%\Users) do (
powershell.exe Clear-DnsClientCache
@echo [1m[33mClosing and restarting Explorer, shutting down Explorer Locked files by restarting Windows Explorer.[0m
rem Taskkill /f /im Explorer.exe >nul
rem Start Explorer.exe >nul
rem Taskkill /f /im msedge.exe >nul
rem @echo Y|%systemroot%\System32\cleanmgr.exe /VERYLOWDISK >nul
@echo. [36m
@echo Creating cleanmgr new entries to clean. & @echo off
powershell.exe New-Item -Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches' -Name 'Prefetch' -ErrorAction SilentlyContinue >nul
powershell.exe New-Item -Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches' -Name 'EdgeCache' -ErrorAction SilentlyContinue >nul
@echo Y|REG IMPORT "%~dp0dir\reg.reg" >nul

@echo R|powershell.exe -File "%~dp0dir\1.ps1"

del /F /S /Q "%userprofile%\AppData\Local\Microsoft\Edge\User Data\Default\Cache\Cache_Data\*" >nul
del /F /S /Q "%SystemDrive%\temp\*" >nul
del /F /S /Q "%systemroot%\temp\*" >nul
del /F /S /Q "%systemroot%\Prefetch\*" >nul
del /f /s /q "%systemdrive%\*\*.tmp" >nul
del /f /s /q "%systemdrive%\*\*\*.tmp" >nul
del /f /s /q "%systemdrive%\*\*\*\*.tmp" >nul
del /f /s /q "%systemdrive%\*\*\*\*\*.tmp" >nul
del /f /s /q "%systemdrive%\*\*\*\*\*\*.tmp" >nul
del /f /s /q "%systemdrive%\*\*\*\*\*\*\*.tmp" >nul
del /f /s /q "%systemdrive%\*\*\*\*\*\*\*\*.tmp" >nul
del /F /S /Q "%temp%\*" >nul
del /F /S /Q "%temp%\*\*" >nul
del /F /S /Q "%temp%\*\*\*" >nul
del /F /S /Q "%temp%\*\*\*\*" >nul
del /F /S /Q "%temp%\*\*\*\*\*" >nul
del /F /S /Q "%temp%\*\*\*\*\*\*" >nul
)
powershell.exe "Set-ExecutionPolicy Default -force" >nul
mode con cols=100 lines=9 &color 09
cls
@echo.
set Msg=System will reboot in 12 secs! Counting
:Update_BAR
cls
set /a FULL+=1
set BAR=%BAR%# 
set /a NB_BAR+=1
echo. &echo.
rem echo %BAR%
echo                         %Msg%... %NB_BAR% seconds
echo  %BAR%
echo. 
if %FULL%==10 goto :END_BAR
@ping localhost -n 1 >nul

Timeout /T 1 /nobreak>nul
goto :Update_BAR

:END_BAR
Shutdown -r /t 2
endlocal
exit /b

:: END
