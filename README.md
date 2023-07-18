MİMARİYE UYGUN MODÜLLERİN OLUŞTURULMASI 



A. MODÜLLERİN OLUŞTURULMA TEKNİĞİ:
	1. Modüller VS Code üzerinde ilgili kod parçacıklarının dockarize edilip, Holstain Registry’ye push edilmesi ve ardından Portal üzerinden add modül fonksiyonu kullanılarak pull edilmesi tekniğiyle oluşturulmuştur.
	2. Azure ARM tekniği, Vs code üzerinde IoT HUB ve IoT edge fonksiyonlarının aktif olmaması üzerine kullanılamamıştır.
B.  MİMARİYE UYGUN MODÜLLERİN KODLARI ÜZERİNDE DÜZENLEME YAPILMASI, IMAJLARININ OLUŞTURULMASI, REGISTRY’YE GÖNDERİLMESİ(PUSH):	
1.	SENSOR MODULE: 
a.	Modülde bir değişiklik yapılmamıştır. IoT edge üzerindeki mevcut modülün kullanılması planlanmıştır. 
b.	Route bölümünde SENSOR MODULE uçları hem SERVER MODULE hem de yeni oluşturulan ModbusServer_Mithat ile irtibatlı olacak şekilde düzenlenmiştir.

2.	SERVER MODULE:
a.	Old Version Kaynak Kodlarındaki (ARM Template) Modbus server kodu esas alınmıştır.
b.	Kaynak kodu içerisindeki Analytic kodlar ayıklanmış ve Analitic modülde kullanılmak üzere ayrılmıştır.
c.	Yeni kod, dockarize edilerek imajı, “imgserver” ismiyle oluşturulmuş, imaj Holstainregisty’ye gönderilmiştir. 
d.	Kullanılan Kodlar;
İmaj oluşturma: “docker build -f Dockerfile.arm64v8 -t imgserver:latest .”
Tag Tanımlama: “docker tag imgserver:latest holsteinregistry.azurecr.io/imgserver:latest”
Registry’ye Gönderme: “docker push holsteinregistry.azurecr.io/imgserver:latest”

3.	CLIENT MODULE:
a.	Çalışmanın en başında gönderilen Client kodu kullanılmıştır.
b.	IP ve Port Numarası Server ile uyumlu halde düzenlenmiştir.
c.	Kodun yukarıda bahsedildiği şekilde imajı “imgclientnew” ismiyle alınmış, registry’ye kaydedilmiştir. 
 
4.	ANALYTIC MODULE:
a.	Old version Modbus kodu üzerindeki analytic hususlar esas alınmıştır.
b.	Bu kodlar ile yeni ve bağımsız bir kod parçacığı oluşturulmuştur. 
c.	Kod, dockarize edilerek “imganalytic” ismiyle imajı alınmış, ilgili Azure Portalı üzerindeki registry’ye gönderilmiştir.
d.	Imajları hazırlanan kodların registry’deki kayıtları aşağıda gösterilmiştir.


C. MODÜLLERİN IOT EDGE ÜZERİNDE OLUŞTURULMASI:
	1.  Holsteinregistry’ye kayıdı yapılan imajlar, Azure portal üzerinden tek tek IoT Edge üzerine deploy edilmiş ve Modüller yeni isimleriyle oluşturulmuştur. (ModbusServer_Mithat, ModbusClient_Mithat, Analytic_Mithat)
	2. IoT Edge üzerinde mevcut Sensor Module ve Server Module silinmemiş, faal halde bırakılmıştır.
	3. Yeni oluşturulan modüller halen faal (“running”) olarak IoT edge üzerinde konumlanmıştır.














D. MODÜLLER OLUŞTURURKEN BİRBİRİYLE İRTİBATLANDIRMALARI:
	1. Modüller oluşturulurken ROUTE üzerinden yukarıdaki mimariye uygun olacak şekilde birbirileriyle irtibatlandırılmıştır. 
	2. İrtibatlandırma ile ilgili detay aşağıda sunulmuştur.


 











E. PC ÜZERİNDE KURULU MODBUS CLIENT’IN ÇALIŞTIRILARAK IoT EDGE İLE İRTİBATA YÖNELİK TEST SONUCUNUN GÖRÜLMESİ:
