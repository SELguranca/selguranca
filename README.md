# SELgurança

## Introdução
Este repositório foi confeccionado para a disciplina de Projetos de Sistemas Digitais SEL0373 do departamento de engenharia elétrica e computação, da escola de engenharia de São Carlos, da Universidade de São Paulo.

## Objetivo
O objetivo do projeto é criar um sistema de segurança de acesso remoto, utilizando um sistema embarcado conectado a um servidor web, podendo ser acessado pela internet de qualquer lugar do planeta.

## Produção

### Hardware
Para a confecção do projeto foram utilizados uma RaspBerry PI 3B+, para a criação do servidor e controle dos periféricos, com o uso de sua RaspCAM, para visualização das imagens, Servomotores, para o controle do ângulo da câmera, Level-Shifter SKU:AC-LLC8-V2, para os pinos de GPIO do microcomputador terem a tensão correta de controle do microcontrolador, através do PWM implementado em Hardware.

![Vista Frontal do projeto](https://github.com/SELguranca/selguranca/blob/Documentation/images/RASP_VF.jpeg)

![Vista Lateral do projeto](https://github.com/SELguranca/selguranca/blob/Documentation/images/RASP_VLE.jpeg)

### Software
Em nível de Software, foram utilizados os projetos implementados neste repositório, para criação de um servidor web feito em flask, a partir da linguagem Python, além disso, para a identificação de pessoas nas imagens, foi utilizado o sistema de visão computacional OpenCV, a partir do método de identificação de pedestres, Histogram Object Gradient (HOG), por este motivo, o algoritmo é capaz de identificar pessoas e devolver as coordenadas do objeto detectado a partir das coordenadas da imagem, permitindo a visualização de bordas da imagem. Além disso, foi utilizado um script para receber os dados do servidor e alterar os ângulos dos servomotores, a partir do PWM, utilizando o PWM de hardware do microcomputador, visto que a biblioteca padrão do sistema operacional não permitia o controle sem oscilação de alta frequência, que dificualtaria a visualiaação da imagem e do processamento de visão computacional. Para o controle dos dados e armazenamento de um histórico de acesso aos ambientes, assim como realizar a notificação de acessos, foi utilizado um banco de dados, implementado em SQLite3, com integração ao servidor web flask. Para a comunicação entre o servidor e o restante do sistema foi utilizado os protocolos de comunicações de redes denominados HTTP (Hyper Text Transfer Protocol), a partir dos métodos de comunicação GET e POST, e para a comunicação com o banco de dados foram utilizados GET e POST, e por limitações do flask, os métodos UPDATE e DELETE, foram implementados como actions do método POST, a partir do JSON enviado no método.

![SPACEMACS Codes](https://github.com/SELguranca/selguranca/blob/Documentation/images/SUPER_SPACE_MACS.png)

### Sistema Operacional
Para o controle de todos os sistemas no microcomputador RaspBerry PI 3B+, foi utilizado um sistema operacional embarcado chamado de RaspBian, baseado na distribuição Debian, feito a partir do kernel Linux, otimizado para o uso em sistemas embarcados baseados nos chips ARM-CORTEX e placas RASP.

![No Graphics SO](https://github.com/SELguranca/selguranca/blob/Documentation/images/OSOS.jpeg)

### Página WEB
Para a visualização da página WEB, o servidor foi alocado na rede da universidade de São Paulo, permitindo o acesso via internet, e o seu layout foi produzido a partir do framework bootstrap 3, que permite integrar o HTML e o CSS, para que a visualização do layout possa ser feita de forma responsiva, alterando o tamanho das janelas a depender da resolução do ambiente de visualização, para a escolha do framework, foram avaliados opções disponíveis e escolhido o bootstrap pelo seu menor tempo de implementação, qualidade dos resultados obtidos e facilidade de acesso a ferramenta.

As funcionalidades da página incluem a visualização da imagem obtida da câmera, o controle dos botôes de manipulação dos servos para controle manual ou de varreduras horizontais e verticais, e a visualização do ângulo de apontamento dos servomotores, além disso, a integração com o banco de dados para mostrar o histórico de acessos ao ambiente, com o horário e posição da câmera, além de uma foto do momento do alerta.

![Página WEB](https://github.com/SELguranca/selguranca/blob/Documentation/images/WEBAGE.jpeg)

<p align = "center">
<img src="https://github.com/zenitheesc/Alcantara_v.1.0/blob/main/Other_Files/Images/Diagram.png"/>
</p>