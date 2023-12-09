from urllib.parse import unquote
from email.mime import base
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from flask_openapi3 import Info, Tag
from flask_openapi3 import OpenAPI
from flask_cors import CORS
from flask import redirect
from model import Session,Fundo,Cota,Portfolio
from logger import logger
from schemas import *
from schemas.fundo import *
from schemas.cota import *
from schemas.portfolio import *
from carga import DadosCVM,gerar_lista_meses
from flask import  render_template, request, redirect, url_for, session
from sqlalchemy import or_,extract
from sqlalchemy.orm import contains_eager
from util import DiaUtil
from dateutil.relativedelta import relativedelta



info = Info(title="Api Fundos", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
atualiza_tag = Tag(name="Atualiza", description="Download e atualização dos dados")
fundo_tag = Tag(name="Fundo", description="Visualização de fundos")
cota_tag = Tag(name="Cota", description="Visualização de Cotas")
portfolio_tag = Tag(name="Portfolio", description="Visualização de Portfolio")
topfund_tag = Tag(name="Top Fundos", description="Melhores Fundos")

@app.get('/')
def home():
    return redirect('/openapi')


@app.post('/atualiza', tags=[atualiza_tag],
          responses={"200": AtualizaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def atualiza_dados(form: AtualizaSchema):
    """Atualiza os dados de acordo com a tarefa selecionada

    Retorna o status da execução da tarefa.
    """
    startdate=form.datainicial
    enddate=form.datafinal
    descricao_job=form.tarefa
    
    logger.debug(f"Executando o job: '{descricao_job}'.")
    try:
        c = DadosCVM()
        count = 0
        if descricao_job == 'portfolio':
            lista_fundos = c.getFundosValidos()
            datas = gerar_lista_meses(startdate,enddate)
            
            for dt in datas:
                c.deleteTableData('portfolio',dt)
                count+= c.loadDadosPortfolio(dt,lista_fundos)
            logger.debug(f"Job '{descricao_job}' executado.")
        elif descricao_job == 'cota':
            lista_fundos = c.getFundosValidos()
            datas = gerar_lista_meses(startdate,enddate)
            
            for dt in datas:
                c.deleteTableData('cota',dt)
                count+= c.loadDadosCotas(dt,lista_fundos)
            logger.debug(f"Job '{descricao_job}' executado.")
        elif descricao_job == 'cadastro':
            c.cleanTableData('fundo')
            count+= c.loadDadosFundos()
        else:
            raise Exception("Job não encontrado")
        return resultado_atualizacao((descricao_job,"OK",count)), 200  
    except Exception as e:
        error_msg = f"Erro na execução do job '{descricao_job}'."
        logger.warning(f"Erro ao executar o job '{descricao_job}', {e}")
        return {"message": error_msg,"description":str(e)}, 400


@app.get('/topfunds', tags=[cota_tag],
         responses={"200": FundoListaViewSchema, "404": ErrorSchema})
def get_top5_fundo(query: BuscaTopFiveSchema):
    """Faz a busca por uma lista de fundos a partir do cnpj do fundo ou do nome do fundo.

    Retorna as características dos fundos solicitados.
    """
    data_inicial = query.data_inicial
    data_final = query.data_final
    classe = query.classe


    d = DiaUtil()

    data_inicial = d.calculadiautil(data_inicial,0)
    data_final = d.calculadiautil(data_final,0)

    session = Session()
   
    logger.debug(f"Busca dos top 3 fundos da classe #{classe}")

    fundos_cotas = session.query(Fundo).join(Fundo.cota) \
                    .options(contains_eager(Fundo.cota)) \
                    .filter(Fundo.classe_fundo==classe,Cota.dt_comptc.in_([data_inicial,data_final])).all()

    df = pd.DataFrame([{'cnpj':f.cnpj,'razao_social':f.razao_social,'classe':f.classe_fundo,'gestor':f.gestor, \
      'vl_cota':[f.cota[0].vl_cota,f.cota[1].vl_cota],'dt_comptc':[f.cota[0].dt_comptc,f.cota[1].dt_comptc]} \
        for f in fundos_cotas if len(f.cota)==2])
    
    df = df.explode(['vl_cota','dt_comptc'])

    df = df.sort_values(by=['cnpj', 'dt_comptc'])
    df['vl_cota_ant'] = df.groupby(['cnpj'])['vl_cota'].shift(1)
    df['rent'] = df['vl_cota']/df['vl_cota_ant'] -1
    df = df.sort_values(by=['rent'],ascending=False)

    fundos_cotas = [f for f in fundos_cotas if f.cnpj in df.head(3)['cnpj'].values]

    if not fundos_cotas:
        error_msg = "Fundo não encontrado na base :/"
        #logger.warning(f"Erro ao buscar fundo pelos dados'{cnpj,tag}', {error_msg}")
        return {"message": error_msg}, 400
    else:
        logger.debug(f"Produto econtrado: '{[f.cnpj for f in fundos_cotas]}'")
        return apresenta_lista_fundos(fundos_cotas), 200

@app.get('/fundo', tags=[fundo_tag],
         responses={"200": FundoListaViewSchema, "404": ErrorSchema})
def get_fundo(query: BuscaFundoSchema):
    """Faz a busca por uma lista de fundos a partir do cnpj do fundo ou do nome do fundo.

    Retorna as características dos fundos solicitados.
    """
    cnpj = query.cnpj
    tag = query.razao_social
    session = Session()
    if cnpj is None:
        logger.debug(f"Busca pelo cnpj, coletando dados sobre o fundo #{cnpj}")
        search = "%{}%".format(tag)
        fundos = session.query(Fundo).filter(Fundo.razao_social.like(search)).all()
    else:
        logger.debug(f"Busca pelo nome, coletando dados sobre o fundo #{tag}")
        fundo = session.query(Fundo).filter(Fundo.cnpj == cnpj).first()
        fundos = [fundo]
    if not fundos:
        error_msg = "Fundo não encontrado na base :/"
        logger.warning(f"Erro ao buscar fundo pelos dados'{cnpj,tag}', {error_msg}")
        return {"message": error_msg}, 400
    else:
        logger.debug(f"Produto econtrado: '{[f.cnpj for f in fundos]}'")
        return apresenta_lista_fundos(fundos), 200


@app.post('/cota', tags=[cota_tag],
         responses={"200": CotaListaViewSchema, "404": ErrorSchema})
def get_cota(form: BuscaCotaSchema):
    """Faz a busca das cotas de um fundo em um intervalo de datas.

    Retorna o valor das cotas no intervalo definido para o fundo especificado.
    """
    json = form.model_dump()
    lista_fundos = json.get('lista_cnpj')
    data_inicial = json.get('data_inicial')
    data_final = json.get('data_final')
    session = Session()
    
    #logger.debug(f"Busca pelo nome, coletando dados sobre o fundo #{tag}")
    #cotas = session.query(Cota).filter(Cota.cnpj == cnpj,Cota.dt_comptc >= data_inicial,Cota.dt_comptc <= data_final).all()
    fundos_cotas = session.query(Fundo).join(Fundo.cota) \
        .options(contains_eager(Fundo.cota)) \
        .filter(Fundo.cnpj.in_(lista_fundos),Cota.dt_comptc >= data_inicial,Cota.dt_comptc <= data_final).all()
    #cotas = [f.cota for f in fundos]
    if not fundos_cotas:
        error_msg = "Não existem cotas no intervalo de datas para o fundo especificado :/"
        logger.warning(f"Erro ao buscar fundo pelos dados'{lista_fundos,data_inicial,data_final}', {error_msg}")
        return {"message": error_msg}, 400
    else:
        logger.debug(f"Cotas encontradas para o fundo: '{lista_fundos}'")
        return apresenta_lista_cotas(fundos_cotas), 200



@app.post('/portfolio', tags=[portfolio_tag],
          responses={"200": PortfolioFundosViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def get_portfolio(form: BuscaPortfolioSchema):
    """Faz a busca da composição da carteira de uma lista de fundos em um intervalo especificado

    Retorna a composição da carteira para os fundos selecionados no período desejado
    """
    data_referencia=form.data_referencia
    lista_fundos=form.lista_cnpj    

    session = Session()
    
    data_inicial = data_referencia + relativedelta(months=-1)
    data_final = data_referencia + relativedelta(months=1)

    fundos = session.query(Fundo).join(Fundo.portfolio) \
                .options(contains_eager(Fundo.portfolio)) \
                .filter(Fundo.cnpj.in_(lista_fundos),Portfolio.dt_comptc > data_inicial, \
                         Portfolio.dt_comptc < data_final).all()
    
    df_total = pd.DataFrame()
    for f in fundos:
        df = pd.DataFrame(query_to_dict(f.portfolio))
        df = df.sort_values(by=['cd_ativo', 'dt_comptc'])
        df['dt_comptc_ant'] = df.groupby(['cd_ativo'])['dt_comptc'].shift(1)
        df['vl_merc_pos_final_ant'] = df.groupby(['cd_ativo'])['vl_merc_pos_final'].shift(1)
        df['vl_resultado'] = df['vl_merc_pos_final'] - df['vl_merc_pos_final_ant'] + df['vl_negociado']
        df=df.dropna()
        lista_datas = df['dt_comptc_ant'].unique()
        dict_pl = dict([(l,max(f.cota, key=lambda obj: obj.dt_comptc if obj.dt_comptc  <= l else datetime(1900,1,1)).vl_patrim_liq) for l in lista_datas])
        df['pl_ref'] = [dict_pl[dt] for dt in df['dt_comptc_ant']]
        df['PnL'] = df['vl_resultado']*100/df['pl_ref'] 
        df['razao_social'] = f.razao_social
        df['absPnL'] = abs(df['PnL'])
        df.sort_values(by=['absPnL'],inplace=True)
        df = df.head(10)
        if len(df_total)==0:
            df_total = df
        else:
            df_total = pd.concat([df_total,df])

    return apresenta_lista_portfolio(df_total),200

