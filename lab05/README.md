
# Sintaxe para executar a aplicação:

```
./main.py server-port max-peers peer-ip:port
```

Parameter | Value | Type | Description
--- | --- | --- | ---
`server-port` | 9991 | int | Porta local selecioada para executar o servidor desse peer
`max-peers` | 0 | int | Número máximo de peers aceito. Se for 0, aceita um valor ilimitado de conexões.
`peer-ip:port` | 192.168.0.103:9991 | string | Peer tracker inicial.
