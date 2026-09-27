# Gerador de Dados de Geoprocessamento com Streamlit

Aplicação Python para:

- gerar dados geográficos fictícios;
- criar geometrias Point ou Polygon;
- gerar atributos associados aos objetos;
- exportar os dados no padrão GeoJSON;
- visualizar os dados em um mapa interativo;
- clicar nos objetos do mapa para consultar os atributos.

## 1. Criar ambiente virtual

Windows:

```cmd
python -m venv venv
venv\Scripts\activate
```

## 2. Instalar dependências

```cmd
pip install -r requirements.txt
```

## 3. Executar

```cmd
streamlit run app.py
```

A aplicação será aberta no navegador.

## Dados padrão

O exemplo inicia próximo de João Pessoa/PB:

Latitude: -7.1195
Longitude: -34.8450

Você pode alterar a latitude, longitude, quantidade e raio diretamente no painel lateral.

## Estrutura GeoJSON

O arquivo gerado segue o padrão:

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [-34.84, -7.12]
      },
      "properties": {
        "id": 1,
        "nome": "Ponto 1",
        "categoria": "Comercial"
      }
    }
  ]
}
```
