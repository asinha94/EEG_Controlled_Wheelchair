
    %Clear Screen
    clc;
    %Clear Variables
    clear all;
    %Close figures
    close all; 
    
    %Preallocate buffer
    data = zeros(153600,13);
    

    %Comport Selection
    portnum1 = 6;  
    %COM Port #
    comPortName1 = sprintf('\\\\.\\COM%d', portnum1);


    % Baud rate for use with TG_Connect() and TG_SetBaudrate().
    TG_BAUD_115200  =   115200;

    % Data format for use with TG_Connect() and TG_SetDataFormat().
    TG_STREAM_PACKETS =     0;
    % Data type that can be requested from TG_GetValue().
    
    TG_DATA_POOR_SIGNAL =     1;
    TG_DATA_ATTENTION =       2;
    TG_DATA_MEDITATION =      3;
    TG_DATA_RAW =             4;
    TG_DATA_DELTA =           5;
    TG_DATA_THETA =           6;
    TG_DATA_ALPHA1 =          7;
    TG_DATA_ALPHA2 =          8;
    TG_DATA_BETA1 =           9;
    TG_DATA_BETA2 =          10;
    TG_DATA_GAMMA1 =         11;
    TG_DATA_GAMMA2 =         12;
    
    %load thinkgear dll
    loadlibrary('Thinkgear.dll');
    
    %To display in Command Window
    fprintf('Thinkgear.dll loaded\n');
    
    
    %get dll version
    dllVersion = calllib('Thinkgear', 'TG_GetDriverVersion');
    
    %To display in command window
    fprintf('ThinkGear DLL version: %d\n', dllVersion );

    % Get a connection ID handle to ThinkGear
    connectionId1 = calllib('Thinkgear', 'TG_GetNewConnectionId');
    if ( connectionId1 < 0 )
        error( sprintf( 'ERROR: TG_GetNewConnectionId() returned %d.\n', connectionId1 ) );
    end;


    % Attempt to connect the connection ID handle to serial port "COM3"
    errCode = calllib('Thinkgear', 'TG_Connect',  connectionId1,comPortName1,TG_BAUD_115200,TG_STREAM_PACKETS );
    if ( errCode < 0 )
        error( sprintf( 'ERROR: TG_Connect() returned %d.\n', errCode ) );
    end

    fprintf( 'Connected.  Reading Packets...\n' );

    
    i=0;
    j=0;
   
    %To display in Command Window

    disp('Reading Brainwaves');

    figure;
    while i < 153600
        
        if (calllib('Thinkgear','TG_ReadPackets',connectionId1,1) == 1)   %if a packet was read...
            if (calllib('Thinkgear','TG_GetValueStatus',connectionId1,TG_DATA_RAW ) ~= 0) 
                j = j + 1;
                i = i + 1;
                %Read attention Valus from thinkgear packets
                
                %timestamp
                data(i,1) = now;
                %Poor Signal
                data(i,2) = calllib('Thinkgear','TG_GetValue',connectionId1,TG_DATA_POOR_SIGNAL );
                %Raw Data
                data(i,3) = calllib('Thinkgear','TG_GetValue',connectionId1,TG_DATA_RAW );
                %Attention
                data(i,4) = calllib('Thinkgear','TG_GetValue',connectionId1,TG_DATA_ATTENTION);
                %Meditation
                data(i,5) = calllib('Thinkgear','TG_GetValue',connectionId1,TG_DATA_MEDITATION );
                %DELTA
                data(i,6) = calllib('Thinkgear','TG_GetValue',connectionId1,TG_DATA_DELTA );
                %THETA
                data(i,7) = calllib('Thinkgear','TG_GetValue',connectionId1,TG_DATA_THETA );
                %ALPHA1
                data(i,8) = calllib('Thinkgear','TG_GetValue',connectionId1,TG_DATA_ALPHA1 );
                %ALPHA2
                data(i,9) = calllib('Thinkgear','TG_GetValue',connectionId1,TG_DATA_ALPHA2 );
                %BETA1
                data(i,10) = calllib('Thinkgear','TG_GetValue',connectionId1,TG_DATA_BETA1 );
                %BETA2
                data(i,11) = calllib('Thinkgear','TG_GetValue',connectionId1,TG_DATA_BETA2 );
                %GAMMA1
                data(i,12) = calllib('Thinkgear','TG_GetValue',connectionId1,TG_DATA_GAMMA1 );
                %GAMMA2
                data(i,13) = calllib('Thinkgear','TG_GetValue',connectionId1,TG_DATA_GAMMA2 );
                
                
                %To display in Command Window
                %disp(data_miditation(i));
               
                %Plot Graph
                %plot(data_att(2,:));
                
                %title('Attention');
                %Delay to display graph
                %pause(.5);
            end
       end
    end
    
    %To display in Command Window
    disp('Loop Completed')
    %Release the comm port
    csvwrite('meditation1.csv',data)
    plot(data(:,1),data(:,2:end));
    legend('Poor Signal','Raw Data','Attention','Meditation','Delta','Theta','Alpha1','Alpha2','Beta1','Beta2','Gamma1','Gamma2')
    calllib('Thinkgear', 'TG_FreeConnection', connectionId1 );