

function csv2fft=Prediction_Use_FFT_Top20Percent_WOFigure(accessMeasurement)
close all;


 %disable output file visibility,just save it anyway
figure('Visible','off')


fileDir=strcat('./',accessMeasurement);
fileDir=strcat(fileDir,'/');
files=dir(strcat(fileDir,'*.csv'));

%to keep each ID and prediction PM25 value
predictionMatrix={};


%get the prediction from each csv 
for fileIndex = 1:size(files,1)
        %disp(files(fileIndex).name)
        
        fileDir=strcat(fileDir,files(fileIndex).name);

        A = csvread(fileDir);
        y = A(:,2).';
       %get all raw pm2.5 data as known history data
        historyPM25=y
       
        
        
        %keep----------
        Fs = length(historyPM25);            % Sampling frequency
        T = 1/Fs;             % Sampling period
                  % Length of signal
        L=length(historyPM25)
        t = (0:L-1)*T;        % Time vector
        %keep------------
        Y = fft(historyPM25);	
        %keep-----
        P2 = abs(Y/L);
        P1 = P2(1:L/2+1);
        P1(2:end-1) = 2*P1(2:end-1);
        %keep------
        
        %keep-----
        f = Fs*(0:(L/2))/L;
        %{
        axFFT=subplot(2,1,1)
        plot(f(1:round(length(f)*0.1)),P1(1:round(length(P1)*0.1)))
        %ylim(axFFT,[0 20])
        title('Single-Sided Amplitude Spectrum of X(t)')
        xlabel('f (Hz)')
        ylabel('|P1(f)|')
        %}

        %find local maximum that frequency > 100
        localMinimaThreshold=0.1
        [pks,locs]=findpeaks(P1,'MinPeakHeight',localMinimaThreshold);

        %sort peaks of the abs(fft(y)) result that exceed 900
        [peakAmplitude peakOrder] = sort(pks, 'descend');
         %text(locs+.02,pks,num2str((1:numel(pks))'));
        
        TopKpercent=0.2
        peakOrder=peakOrder(1:round(size(peakOrder,2)*TopKpercent))
        peakAmplitude=peakAmplitude(1:round(size(peakAmplitude,2)*TopKpercent))


        phase=[]
        for Topn= 1:length(peakOrder)
            phase = [ phase angle(Y(locs(peakOrder(Topn))))]
        end
        %phase = angle([Y(11) Y(51) Y(101)])

        % predict
        lengthOfPredictionTimes=2;
        time = (0:L*lengthOfPredictionTimes-1)*T;
        modelfunction=0;
        for Topn=1:length(phase)
            modelfunction = modelfunction+(peakAmplitude(Topn)*cos(2*pi*(locs(peakOrder(Topn))-1)*time+phase(Topn)))
        end
       modelfunction=modelfunction+P1(1)
        %plot 1st most influential frequency
        %{
        axFirstFre=subplot(2,1,2);
        plot(axFirstFre,length(historyPM25)*time(1:length(time)),modelfunction(1:length(time)),'r') 
        hold on
        %plot(axFirstFre,1000*time(1:length(time)),modelfunction(1:length(time)),'r')
       %keep------
       %}
       

        
        
  

    
       
        
         
            
         
            
            
           
           
            
           %{ 
            %xData = get(axSampleNum,'XData');
           % set(gca,'Xtick',linspace(xData(1),xData(end),numberOfXTicks))
            
            %Fig title
            FigTitle=strcat(accessMeasurement,'--');
            FigTitle=strcat(FigTitle,files(fileIndex).name);
            FigTitle=strcat(FigTitle,' Frequency in [2:First 10% of 80%PM2.5_data]  which >100');
            
            
            title(FigTitle);
         %draw PM2.5 raw data
         plot(axFirstFre,y)
         %}



        
         
        
       

        
      
  
        
        %plot TOP20 repetition
       
        %plot sum of Top20
        %plot(axFirstFre,real(sumTop20_percent)),grid on
        
        %plot the rest
        %TheRest=historyPM25-real(sumTop20_percent);
        %plot(axFirstFre,TheRest),grid on
        
       
        %plot(t(M+1:P),predictTop20(M+1:P));
        
        
        
        
        
        %plot(t(M+1:P),predictTheRest(M+1:P));
       
        
        
        
         %{
        %figure label setting
        ylim(axFirstFre,[-50 200])
        legend('TOP20%','PM2.5','Location','NorthEast')
        legend('boxoff')
       %}
%set(gca,'XTick',1:interval:length(aftercat),'XTickLabel',screen)

       %{
        title1=files(fileIndex).name;
        title1=strcat(title1,'  原始PM2.5、TOP20及剩下的頻率之IFFT混合圖型');
        title(title1);
        %}
        
        %draw the division line
        l = line(length(historyPM25)*[1 1], get(gca, 'ylim'));
        set(l, 'color', [0,0,0]);
        
        
        %draw diff 
        %{
        subplot(3,1,3);
        y=y(1:length(modelfunction))
        diff=abs(y-modelfunction)
        plot(length(historyPM25)*time(length(historyPM25):length(time)),diff(length(historyPM25):length(diff)),'g')
       
        disp(modelfunction(length(historyPM25)+124))
        %}
        
        %append the current ID and its prediction of 144th prediction to
        %prediction output matrix
        
        %predictionMatrix=[predictionMatrix;files(fileIndex).name,modelfunction(length(historyPM25)+144)]
        predictionPointX=length(historyPM25)
        
        %get prediction of the next 12 hrs
        next12HRPrediction={}
        %used to detect ID with few data ,which should be ignored
        ignore=0;
        for hr=1:12
            % detect ID with few data ,which should be ignored
            if((predictionPointX+hr*12)>length(modelfunction))
                ignore=1
                break
            
            else
                next12HRPrediction=[next12HRPrediction,modelfunction(predictionPointX+hr*12)]
            end
        end
        
        %if bad ID is detected,skip this ID
       if(ignore==1)
           %reset csv fileDir 
           fileDir='';
           fileDir=strcat('./',accessMeasurement);
           fileDir=strcat(fileDir,'/');
           continue
       end
        
        %extract Device_ID from filename
        [Device_id,rest]=strtok(files(fileIndex).name,'.')
        %predictionMatrix{end+1}={files(fileIndex).name,modelfunction(predictionPointX)};
        predictionMatrix=[predictionMatrix,Device_id,next12HRPrediction(1),next12HRPrediction(2),next12HRPrediction(3),next12HRPrediction(4),next12HRPrediction(5),next12HRPrediction(6),next12HRPrediction(7),next12HRPrediction(8),next12HRPrediction(9),next12HRPrediction(10),next12HRPrediction(11),next12HRPrediction(12)];
        %IDMatrix=[IDMatrix;files(fileIndex).name]
        %mark the 144th point
         %{
          plot(predictionPointX,modelfunction(predictionPointX),'bo');   
         hold off
        %}



        
      
    
        
        
        %reset csv fileDir 
       fileDir='';
       fileDir=strcat('./',accessMeasurement);
       fileDir=strcat(fileDir,'/');
      
       
        %save output as png image in the accessMeasurement folder
        %{
        outputFilename=strcat(accessMeasurement,'_');
        outputFilename=strcat(outputFilename,files(fileIndex).name);
        outputFilename=strcat(outputFilename,'.png');
        outputFilename=strcat(fileDir,outputFilename);
        
        saveas(gcf,outputFilename);
        %}
        
        



       



       

end
%output the prediction csv
%csvwrite('E:/predictionPM25/predictionPm25.csv',predictionMatrix)


fid = fopen('E:/predictionPM25/predictionPM25.csv','wt');
 fprintf(fid,'Device_ID,In_1_hr,In_2_hr,In_3_hr,In_4_hr,In_5_hr,In_6_hr,In_7_hr,In_8_hr,In_9_hr,In_10_hr,In_11_hr,In_12_hr\n'); 
for row=1:size(predictionMatrix,1)
   %fprintf(fid,'%s,%f\n',predictionMatrix{row,1:end-1},predictionMatrix{row,1:end});
   fprintf(fid,'%s,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\n',predictionMatrix{row,:});  
end
fclose(fid);

%cell2csv('E:/predictionPM25/predictionPM25_lass.csv',predictionMatrix);
csv2fft=0;
%%%%
