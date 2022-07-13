# SELgurança

## Introdução
Este repositório foi confeccionado para a disciplina de Projetos de Sistemas Digitais SEL0373 do departamento de engenharia elétrica e computação, da escola de engenharia de São Carlos, da Universidade de São Paulo.

## Objetivo
O objetivo do projeto é criar um sistema de segurança de acesso remoto, utilizando um sistema embarcado conectado a um servidor web, podendo ser acessado pela internet de qualquer lugar do planeta.

## Produção

### Hardware
Para a confecção do projeto foram utilizados uma RaspBerry PI 3B+, para a criação do servidor e controle dos periféricos, com o uso de sua RaspCAM, para visualização das imagens, Servomotores, para o controle do ângulo da câmera, Level-Shifter SKU:AC-LLC8-V2, para os pinos de GPIO do microcomputador terem a tensão correta de controle do microcontrolador, através do PWM implementado em Hardware, além disso, foi utilizado uma placa de confecção própria para a conexão dos conectores dos servomotores aos cabos de prototipagem utilizados na rasp.

<p align = "center">
<img src="https://github.com/SELguranca/selguranca/blob/Documentation/images/RASP_VF.jpeg"/>
</p>

<p align = "center">
<img src="https://github.com/SELguranca/selguranca/blob/Documentation/images/RASP_VLE.jpeg"/>
</p>

<p align = "center">
<img src="https://github.com/SELguranca/selguranca/blob/Documentation/images/Schema.jpeg"/>
</p>

### Software
Em nível de Software, foram utilizados os projetos implementados neste repositório, para criação de um servidor web feito em flask, a partir da linguagem Python, além disso, para a identificação de pessoas nas imagens, foi utilizado o sistema de visão computacional OpenCV, a partir do método de identificação de pedestres, Histogram of Oriented Gradient (HOG), por este motivo, o algoritmo é capaz de identificar pessoas e devolver as coordenadas do objeto detectado a partir das coordenadas da imagem, permitindo a visualização de bordas da imagem. Além disso, foi utilizado um script para receber os dados do servidor e alterar os ângulos dos servomotores, a partir do PWM, utilizando o PWM de hardware do microcomputador, visto que a biblioteca padrão do sistema operacional não permitia o controle sem oscilação de alta frequência, que dificualtaria a visualiaação da imagem e do processamento de visão computacional. Para o controle dos dados e armazenamento de um histórico de acesso aos ambientes, assim como realizar a notificação de acessos, foi utilizado um banco de dados, implementado em SQLite3, com integração ao servidor web flask. Para a comunicação entre o servidor e o restante do sistema foi utilizado os protocolos de comunicações de redes denominados HTTP (Hyper Text Transfer Protocol), a partir dos métodos de comunicação GET e POST, e para a comunicação com o banco de dados foram utilizados GET e POST, e por limitações do flask, os métodos UPDATE e DELETE, foram implementados como actions do método POST, a partir do JSON enviado no método.

<p align = "center">
<img src="https://github.com/SELguranca/selguranca/blob/Documentation/images/SUPER_SPACE_MACS.png"/>
</p>

### Sistema Operacional
Para o controle de todos os sistemas no microcomputador RaspBerry PI 3B+, foi utilizado um sistema operacional embarcado chamado de RaspBian, baseado na distribuição Debian, feito a partir do kernel Linux, otimizado para o uso em sistemas embarcados baseados nos chips ARM-CORTEX e placas RASP.

<p align = "center">
<img src="https://github.com/SELguranca/selguranca/blob/Documentation/images/OSOS.jpeg"/>
</p>

### Página WEB
Para a visualização da página WEB, o servidor foi alocado na rede da universidade de São Paulo, permitindo o acesso via internet, e o seu layout foi produzido a partir do framework bootstrap 3, que permite integrar o HTML e o CSS, para que a visualização do layout possa ser feita de forma responsiva, alterando o tamanho das janelas a depender da resolução do ambiente de visualização, para a escolha do framework, foram avaliados opções disponíveis e escolhido o bootstrap pelo seu menor tempo de implementação, qualidade dos resultados obtidos e facilidade de acesso a ferramenta.

As funcionalidades da página incluem a visualização da imagem obtida da câmera, o controle dos botôes de manipulação dos servos para controle manual ou de varreduras horizontais e verticais, e a visualização do ângulo de apontamento dos servomotores, além disso, a integração com o banco de dados para mostrar o histórico de acessos ao ambiente, com o horário e posição da câmera, além de uma foto do momento do alerta.

<p align = "center">
<img src="https://github.com/SELguranca/selguranca/blob/Documentation/images/WEBAGE.jpeg"/>
</p>

## Tutorial

### Hardware
É necessário a confecção de uma placa para a interface de comunicação entre os servos e a raspberry, que pode ser feita em uma placa perfurada, ou uma protoboard, a fim de testes de protótipos, ou em uma placa de circuito impresso para projetos completos.
Além disso deve ser feita a conexão da Rasp a sua fonte de alimentação e os servomotores a uma fonte externa, a fim de manter independente a alimentação do microcomputador e dos servomotores, evitando ruídos.

Além disso, o level-shifter deve ser conectado entre a alimentação da Rasp e da fonte externa, de forma a manter o sinal do pwm dos pinos de GPIO iguais aos valores necessários para a alimentação dos servos.

### Software
Para o uso do software, foi elaborada uma lista com as bibliotecas que devem ser instaladas, para isso, inicializa-se o ambiente virtual em python, e roda a instalação das bibliotecas colocadas nos requirements.txt, além da instalação dos scripts a partir do clone deste repositório. Caso o OpenCV seja inicializado em um sistema sem interface gráfica, como o utilizado neste projeto, deve-se atentar a instalação do openCV correto, detelhado nos requirements.txt.

Além disso, deve-se habilitar o banco de dados, a partir dos scripts disponibilizados no repositório. Além disso, o servidor deve ser hospedado em um domínio, que pode ser pelo IP local, para testes, ou em um servidor dedicado, para a conexão, foi alterado o MAC da placa para um MAC que a rede reconheça como parte do servidor, para o caso do IP, pode-se conectar pelo navegador a partir do "http://endereçoIP/porta/Nome", estes valores de porta e nome podem ser alterados nos scripts do webserver.py.

Alguns tutoriais úteis para o uso do projeto:

Flask, que foi utilizado na confecção do projeto => [documentação do flask](https://flask.palletsprojects.com/en/2.1.x/)

OpenCV, utilizado para o projeto => [documentação do OpenCV](https://learnopencv.com/histogram-of-oriented-gradients/)

SQLite, utilizado para o projeto => [documentação do SQLite3](https://www.sqlite.org/quickstart.html)



### Sistema Operacional
O sistema operacional foi utilizado e instalado a partir do guia oficial da distribuição, instalado em um cartão SD, e conectado a Rasp a partir de seu conector SDcard, a partir disso foi inicializado o sistema e configurado a seguindo o tutorial da distribuição para seu uso, com ela configurada, deve-se clonar o repositório, e inicializar os sistemas do servidor no sistema embarcado.

Alguns tutoriais úteis para o uso da RASP:

RaspBian, utilizado na confecção do projeto => [documentação do RaspBian](http://www.raspbian.org/)

Git na RaspBerry, em caso de dúvidas => [documentação do RaspBian com Git](https://projects.raspberrypi.org/en/projects/getting-started-with-git/12)


### Página WEB

Para a criação do layout da página web, foi utilizado o bootstrap, que deve ser incluído ao projeto, assim como o flask, é um framework para uso das funcionalidades de layout de forma mais responsiva, caso se deseje alterar o design da página, recomenda-se o uso do framework para integração com as partes já utilizados.

BootStrap, utilizado na confecção do projeto => [documentação do BootStrap](https://getbootstrap.com/)

## Implementação do projeto (APRESENTAÇÂO)

A implementação do nosso projeto foi feita dividindo o projeto em etapas como as detalhadas abaixo, isto facilitou o nosso desenvolvimento e a explicação dos componentes do projeto de forma simplificada.

### Hardware

### Conexões

### Level-shifter

### Software

#### HOG

Para identificar pessoas no laboratório foi utilizado a função HOG (Histogram of Oriented Gradients) do framework OpenCV. Este framework também oferece funções para o acesso da câmera e captura dos frames, que então são redimensionados para a sua inserção no algorítmo HOG, que retorna coordenadas que indicam a posição dos indivídos no frame. Essas coordenadas são reescaladas e utilizadas para desenhar retângulos sobre uma determinada região no frame original.

O HOG foi escolhido por conta da sua otimização para uso em aplicações de identificação de pedestres, resultando em melhor velocidade de execução no hardware limitado da Raspberry Pi.

Ao longo do desenvolvimento também experimentamos com algoritimos d tipo Haar Cascade, utilizados para identificação de rostos e partes do corpo, mas estes se mostraram mais onerosos em termos de processamento quando comparados com o HOG.

### Servo

## Sistema operacional

#### Distro

### Threads

### Servidor

### Página WEB

DDDDDDDDDDDDDDDD

## Implementações futuras

Como projetos futuros, o objetivo é implementar o controle de múltiplas câmeras, o controle dos servos de forma autônoma, a partir da coordenada do objeto detectado, o colocando no centro da imagem e o mantendo sempre em foco, implementação em um servidor web fora do domínio de rede da universidade, identificação facial a partir de visão computacional, sistema de usuários, sistema de notificação por email em caso de acessos, melhoria da responsividade do site, e a criação da versão mobile da página e a criação de um aplicativo para uso do sistema, e o desenvolvimento de um tutorial para tornar acessível o uso do sistema e a criação de sistemas a partir deste, para facilitar o uso do projeto por comunidades open-source.