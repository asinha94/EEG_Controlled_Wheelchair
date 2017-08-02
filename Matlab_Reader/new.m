
    %Comport Selection
    portnum1 = 6;  
    %COM Port #
    comPortName1 = sprintf('\\\\.\\COM%d', portnum1);


    % Baud rate for use with TG_Connect() and TG_SetBaudrate().
    TG_BAUD_115200  =   115200;

    % Data format for use with TG_Connect() and TG_SetDataFormat().
    TG_STREAM_PACKETS =     0;
    % Data type that can be requested from TG_GetValue().
    
    TG_DATA_ATTENTION =       2;
    TG_DATA_MEDITATION =      3;
    TG_DATA_BLINK_STRENGTH = 37;
    
    disp('Connectiong to EEG scanner');
    %load thinkgear64 dll
    loadlibrary('thinkgear64.dll','thinkgear64.h');
    
    %To display in Command Window
    fprintf('thinkgear64.dll loaded\n');
    
    
    %get dll version
    dllVersion = calllib('thinkgear64', 'TG_GetDriverVersion');
    
    %To display in command window
    fprintf('thinkgear64 DLL version: %d\n', dllVersion );

    % Get a connection ID handle to thinkgear64
    connectionId1 = calllib('thinkgear64', 'TG_GetNewConnectionId');
    if ( connectionId1 < 0 )
        error( sprintf( 'ERROR: TG_GetNewConnectionId() returned %d.\n', connectionId1 ) );
    end;


    % Attempt to connect the connection ID handle to serial port "COM3"
    errCode = calllib('thinkgear64', 'TG_Connect',  connectionId1,comPortName1,TG_BAUD_115200,TG_STREAM_PACKETS );
    if ( errCode < 0 )
        error( sprintf( 'ERROR: TG_Connect() returned %d.\n', errCode ) );
    end

    fprintf( 'Connected.  Reading Packets...\n' );
    
    if(calllib('thinkgear64','TG_EnableBlinkDetection',connectionId1,1)==0)
        disp('blinkdetectenabled');
    end
    
    disp('Connected to EEG scanner');
    
    %To display in Command Window

    disp('Reading Brainwaves');

    while (1)
        
        if (calllib('thinkgear64','TG_ReadPackets',connectionId1,1) == 1)   %if a packet was read...
            if (calllib('thinkgear64','TG_GetValueStatus',connectionId1,TG_DATA_ATTENTION ) ~= 0) 
                %Read attention Valus from thinkgear packets
                
                %Attention
                data(1) = calllib('thinkgear64','TG_GetValue',connectionId1,TG_DATA_ATTENTION);
                disp('attention:%s', data(1))
                %Meditation
                data(2) = calllib('thinkgear64','TG_GetValue',connectionId1,TG_DATA_MEDITATION );
                disp('meditation:%s', data(2))
                %Eye Blick
                data(3) = calllib('thinkgear64','TG_GetValue',connectionId1,TG_DATA_BLINK_STRENGTH );
                disp('blink:%s', data(3))
                
              
            end
       end
    end
    
    