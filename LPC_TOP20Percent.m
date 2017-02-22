

function csv2fft=LPC_TOP20Percent(accessMeasurement)
close all;


 %disable output file visibility,just save it anyway
figure('Visible','off')


fileDir=strcat('./',accessMeasurement);
fileDir=strcat(fileDir,'/');
files=dir(strcat(fileDir,'*.csv'));
for fileIndex = 1:size(files,1)
        disp(files(fileIndex).name)
        
        fileDir=strcat(fileDir,files(fileIndex).name);

        A = csvread(fileDir);
        y = A(:,2);
        
        %get 80% of pm2.5 data as known history data
        historyPM25=y(1:round(size(y,1)*0.8))
       
        Y = fft(historyPM25);	
        f = abs(Y); 
        
        
        
        
        
  

    
       
        
          %find peaks (ocal maximum that frequency > 900) in the first 10% of result of FFT 
            ax10percentFFT=subplot(2,1,1);
          %find peaks
            FFT=f(2:round(size(f,1)*0.1));
            
            
            %set number of ticks of axis for 10% of PM2.5 after FFT
            numberOfXTicks = 40;                	      
            axSampleNum=plot(FFT,'.-b'); grid on
         
           
            
            
            %find local maximum that frequency > 100
            [pks,locs]=findpeaks(FFT,'MinPeakHeight',100);
            text(locs+.02,pks,num2str((1:numel(pks))'));

          
            set(gca,'XTick',0:100:800, 'fontSize', 8,'fontname', 'Tahoma');
            figureHandle = gcf;
            set(findall(figureHandle,'type','text'),'fontweight', 'bold','fontSize',8,'fontname', 'Tahoma');
            xlabel('Sample points');
            axis([ax10percentFFT],[0,100,0,20000])
            
            
            xData = get(axSampleNum,'XData');
            set(gca,'Xtick',linspace(xData(1),xData(end),numberOfXTicks))
            
            %Fig title
            FigTitle=strcat(accessMeasurement,'--');
            FigTitle=strcat(FigTitle,files(fileIndex).name);
            FigTitle=strcat(FigTitle,' Frequency in [2:First 10% of 80%PM2.5_data]  which >900');
            
            
            title(FigTitle);

        
        
        
     
         % %sort peaks of the abs(fft(y)) result that exceed 900
        [m mi] = sort(pks, 'descend');
        
    %get top 10 of dominate frequency
    
    %if this Device has more than 10 peaks in the first 10% of FFT result
    if size(mi,1)>=20
        %plot 1st most influential frequency
        axFirstFre=subplot(2,1,2);
        
        
        %use timestamp as X axis
        xid = A(:,1)'

x1 = A(:,3)'
x2 = A(:,4)'
x3 = A(:,5)'

ys = A(:,2)

aftercat = {}
for i=1:length(x1)

	id = num2str(xid(i))
	date = num2str(x1(i),'%.2f');
	hour = num2str(x2(i),'%02d');
	minute = num2str(x3(i));
	s = strcat(date,'-',hour,':',minute)
	% s = strcat(id)
	disp(s)
	aftercat{end+1} = s;

	c = class(s)
end


screen = {}
segment = 5
interval = floor(length(aftercat)/(segment))
for i=1:length(aftercat)
	if mod(i,interval) == 1 
		disp(i)
		screen{end+1} = char(aftercat(i));
	% else
	% 	screen{end+1} = ''
	end
end

      
        % end use timestamp as X axis
       
        %draw the result of labelling the peaks in the first 10% of FFT result
         plot(axFirstFre,y)



        
         
        
       

        
        %get top 20percent peaks of result of FFT
        percent=0.2
        sumTop20_percent=0;
        for Topn = 1:round(length(mi)*percent)
             TopnFre=zeros(length(Y),1);
             TopnFre(locs(mi(Topn))-1:locs(mi(Topn)))=Y(locs(mi(Topn))-1:locs(mi(Topn)));
             sumTop20_percent=sumTop20_percent+ifft(TopnFre);
        end
  
        hold on
        %plot TOP20 repetition
       
        %plot sum of Top20
        %plot(axFirstFre,real(sumTop20_percent),'r'),grid on
        
        %{
        %plot the rest
        TheRest=historyPM25-real(sumTop20_percent);
        plot(axFirstFre,TheRest),grid on
        %}
        %plot prediction of sum of Top20
        P=length(y)  %all
        M=length(sumTop20_percent) %the start of prediction
        %N=length(sumTop20_percent)% Order of LPC auto-regressive model
        t=1:P
        predictTop20 = zeros(1, length(y));
        % fill in the known part of the time series
        predictTop20(1:M) = historyPM25(1:M);
        

       
        %%%make LPC prediction 
        %get last 20% of PM2.5 raw data for prediction
        LPCTrainingData=historyPM25(round(size(historyPM25,1)*0.8):length(historyPM25))
        %get mean of last 20% raw data
        meanLast20Raw=mean(LPCTrainingData)
        %filter the high frequency of the last 20% of PM2.5 raw data
        windowSize = 5;
        filterPara_b = (1/windowSize)*ones(1,windowSize);
        filterPara_a = 1;
        LPCTrainingData = filter(filterPara_b,filterPara_a,LPCTrainingData);
        
        % LPC prediction 
        N=length(LPCTrainingData)-1% Order of LPC auto-regressive model
        LPC_Result = lpc( LPCTrainingData, N);

        for ii=(M+1):P      
            predictTop20(ii) = -sum(LPC_Result(2:end) .* predictTop20((ii-1):-1:(ii-N)));
        end
        
        
        
        %add each LPC prediction value with mean of last 20% PM2.5 raw data
        for h=(M+1):P      
            predictTop20(h) =  predictTop20(h)+meanLast20Raw;
        end
       
        %plot LPC prediction
        plot(t(1:P),predictTop20(1:P));
        
        
        
        %{
        %plot prediction of The Rest
        M=length(TheRest) %the start of prediction
        N=length(TheRest)% Order of LPC auto-regressive model
        predictTheRest = zeros(1, length(y));
        % fill in the known part of the time series
        predictTheRest(1:M) = TheRest(1:M);

        LPC_Result = lpc(TheRest, N);
        for ii=(M+1):P      
            predictTheRest(ii) = -sum(LPC_Result(2:end) .* predictTheRest((ii-1):-1:(ii-N)));
        end
        plot(t(M+1:P),predictTheRest(M+1:P));
       %}
         %draw the division line
        l = line(length(historyPM25)*[1 1], get(gca, 'ylim'));
        set(l, 'color', [0,0,0]);
        
        
        
        
        %figure label setting
        ylim(axFirstFre,[-50 200])
        legend('PM2.5','LPC_Prediction','Location','NorthEast')
        legend('boxoff')
        hold off
set(gca,'XTick',1:interval:length(aftercat),'XTickLabel',screen)


xticklabel_rotate([],15,[],'Fontsize',10)       
        title1=files(fileIndex).name;
        title1=strcat(title1,'  原始PM2.5、TOP20及剩下的頻率之IFFT混合圖型');
        title(title1);
       
       



        
      
    end 
        
        
        %reset csv fileDir 
       fileDir='';
       fileDir=strcat('./',accessMeasurement);
       fileDir=strcat(fileDir,'/');
      
       
        %save output as png image in the accessMeasurement folder
        outputFilename=strcat(accessMeasurement,'_');
        outputFilename=strcat(outputFilename,files(fileIndex).name);
        outputFilename=strcat(outputFilename,'.png');
        outputFilename=strcat(fileDir,outputFilename);
        
        saveas(gcf,outputFilename);



       



       

end
csv2fft=0;
%%%%
