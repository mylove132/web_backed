import json


def jmx_header_setting():
    jmx_file_header = '''<?xml version="1.0" encoding="UTF-8"?>
    <jmeterTestPlan version="1.2" properties="3.1" jmeter="3.1 r1770033">
    <hashTree>
        <TestPlan guiclass="TestPlanGui" testclass="TestPlan" testname="测试计划" enabled="true">
        <stringProp name="TestPlan.comments"></stringProp>
        <boolProp name="TestPlan.functional_mode">false</boolProp>
        <boolProp name="TestPlan.serialize_threadgroups">false</boolProp>
        <elementProp name="TestPlan.user_defined_variables" elementType="Arguments" guiclass="ArgumentsPanel" testclass="Arguments" testname="用户定义的变量" enabled="true">
        <collectionProp name="Arguments.arguments"/>
      </elementProp>
      <stringProp name="TestPlan.user_define_classpath"></stringProp>
    </TestPlan>
    '''
    return jmx_file_header


def jmx_control_seeting(pre_num=200, pre_time=120):
    """
    :param pre_num:压测并发数
    :param pre_time: 压测时长
    :return:
    """
    jmx_file_exec_control = '''
    <hashTree>
        <ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="线程组" enabled="true">
            <stringProp name="ThreadGroup.on_sample_error">continue</stringProp>
            <elementProp name="ThreadGroup.main_controller" elementType="LoopController" guiclass="LoopControlPanel" testclass="LoopController" testname="循环控制器" enabled="true">
            <boolProp name="LoopController.continue_forever">false</boolProp>
            <intProp name="LoopController.loops">-1</intProp>
            </elementProp>
            <stringProp name="ThreadGroup.num_threads">{}</stringProp>
            <stringProp name="ThreadGroup.ramp_time">1</stringProp>
            <longProp name="ThreadGroup.start_time">1558058964000</longProp>
            <longProp name="ThreadGroup.end_time">1558058964000</longProp>
            <boolProp name="ThreadGroup.scheduler">true</boolProp>
            <stringProp name="ThreadGroup.duration">{}</stringProp>
            <stringProp name="ThreadGroup.delay"></stringProp>
        </ThreadGroup>
            '''.format(pre_num, pre_time)
    return jmx_file_exec_control


def jmx_http_setting(url, interface_name='http请求', request_type="GET", timeOut=5000, params=''):
    """
    :param url:请求url
    :param interface_name:请求的接口名称
    :param request_type: 请求接口的类型
    :return:
    """
    ul = ''
    if url.find('&') != -1:
        ul = url.replace('&', '&amp;')
    else:
        ul = url
    temp_text = '''
           <elementProp name="{}" elementType="HTTPArgument">
                <boolProp name="HTTPArgument.always_encode">false</boolProp>
                <stringProp name="Argument.value">{}</stringProp>
                <stringProp name="Argument.metadata">=</stringProp>
                <boolProp name="HTTPArgument.use_equals">true</boolProp>
                <stringProp name="Argument.name">{}</stringProp>
              </elementProp>
    '''

    tap_text = '''
   <boolProp name="HTTPSampler.postBodyRaw">true</boolProp>
          <elementProp name="HTTPsampler.Arguments" elementType="Arguments">
            <collectionProp name="Arguments.arguments">
              <elementProp name="" elementType="HTTPArgument">
                <boolProp name="HTTPArgument.always_encode">false</boolProp>
                <stringProp name="Argument.value">{}</stringProp>
                <stringProp name="Argument.metadata">=</stringProp>
              </elementProp>
            </collectionProp>
          </elementProp>
    '''
    tem = ''
    print(params)
    if params:
        if str(params).find('paramskey') != -1:
            for p in json.loads(params):
                key = p['paramskey']
                value = p['paramsvalue']
                if value.find('"') != -1:
                    value = value.replace('"', '&quot;')
                temp = temp_text.format(key, value, key)
                tem += temp

            jmx_http = '''
                <hashTree>
                 <HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="{}" enabled="true">
          <elementProp name="HTTPsampler.Arguments" elementType="Arguments" guiclass="HTTPArgumentsPanel" testclass="Arguments" testname="用户定义的变量" enabled="true">
            <collectionProp name="Arguments.arguments">
              {}
            </collectionProp>
          </elementProp>
          <stringProp name="HTTPSampler.domain"></stringProp>
          <stringProp name="HTTPSampler.port"></stringProp>
          <stringProp name="HTTPSampler.connect_timeout"></stringProp>
          <stringProp name="HTTPSampler.response_timeout">{}</stringProp>
          <stringProp name="HTTPSampler.protocol"></stringProp>
          <stringProp name="HTTPSampler.contentEncoding"></stringProp>
          <stringProp name="HTTPSampler.path">{}</stringProp>
          <stringProp name="HTTPSampler.method">{}</stringProp>
          <boolProp name="HTTPSampler.follow_redirects">true</boolProp>
          <boolProp name="HTTPSampler.auto_redirects">false</boolProp>
          <boolProp name="HTTPSampler.use_keepalive">true</boolProp>
          <boolProp name="HTTPSampler.DO_MULTIPART_POST">false</boolProp>
          <boolProp name="HTTPSampler.monitor">false</boolProp>
          <stringProp name="HTTPSampler.embedded_url_re"></stringProp>
        </HTTPSamplerProxy>
                '''.format(interface_name, tem, timeOut, ul, request_type)
            return jmx_http
        else:
            jmx_http = '''
                            <hashTree>
                                <HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="{}" enabled="true">
                                  {}
                                  <stringProp name="HTTPSampler.domain"></stringProp>
                                  <stringProp name="HTTPSampler.port"></stringProp>
                                  <stringProp name="HTTPSampler.connect_timeout"></stringProp>
                                  <stringProp name="HTTPSampler.response_timeout">{}</stringProp>
                                  <stringProp name="HTTPSampler.protocol"></stringProp>
                                  <stringProp name="HTTPSampler.contentEncoding"></stringProp>
                                  <stringProp name="HTTPSampler.path">{}</stringProp>
                                  <stringProp name="HTTPSampler.method">{}</stringProp>
                                  <boolProp name="HTTPSampler.follow_redirects">true</boolProp>
                                  <boolProp name="HTTPSampler.auto_redirects">false</boolProp>
                                  <boolProp name="HTTPSampler.use_keepalive">true</boolProp>
                                  <boolProp name="HTTPSampler.DO_MULTIPART_POST">false</boolProp>
                                  <boolProp name="HTTPSampler.monitor">false</boolProp>
                                  <stringProp name="HTTPSampler.embedded_url_re"></stringProp>
                                </HTTPSamplerProxy>
                            '''.format(interface_name, tap_text.format(params), timeOut, ul, request_type)
            return jmx_http

    else:
        jmx_http = '''
                        <hashTree>
                            <HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="{}" enabled="true">
                              <stringProp name="HTTPSampler.domain"></stringProp>
                              <stringProp name="HTTPSampler.port"></stringProp>
                              <stringProp name="HTTPSampler.connect_timeout"></stringProp>
                              <stringProp name="HTTPSampler.response_timeout">{}</stringProp>
                              <stringProp name="HTTPSampler.protocol"></stringProp>
                              <stringProp name="HTTPSampler.contentEncoding"></stringProp>
                              <stringProp name="HTTPSampler.path">{}</stringProp>
                              <stringProp name="HTTPSampler.method">{}</stringProp>
                              <boolProp name="HTTPSampler.follow_redirects">true</boolProp>
                              <boolProp name="HTTPSampler.auto_redirects">false</boolProp>
                              <boolProp name="HTTPSampler.use_keepalive">true</boolProp>
                              <boolProp name="HTTPSampler.DO_MULTIPART_POST">false</boolProp>
                              <boolProp name="HTTPSampler.monitor">false</boolProp>
                              <stringProp name="HTTPSampler.embedded_url_re"></stringProp>
                            </HTTPSamplerProxy>
                        '''.format(interface_name, timeOut, ul, request_type)

        return jmx_http


def jmx_response_assert(assert_text=''):
    if assert_text.find('"') != -1:
        assert_text = assert_text.replace('"', '&quot;')
    jmx_response_assert_text = '''
        <hashTree>
          <ResponseAssertion guiclass="AssertionGui" testclass="ResponseAssertion" testname="响应断言" enabled="true">
            <collectionProp name="Asserion.test_strings">
              <stringProp name="67791721">{}</stringProp>
            </collectionProp>
            <stringProp name="Assertion.test_field">Assertion.response_data</stringProp>
            <boolProp name="Assertion.assume_success">false</boolProp>
            <intProp name="Assertion.test_type">16</intProp>
          </ResponseAssertion>
        <hashTree/>
    '''.format(assert_text)
    return jmx_response_assert_text


def jmx_see_result_control():
    """
    查看结果树
    :return:
    """
    result_control_text = '''
    <ResultCollector guiclass="ViewResultsFullVisualizer" testclass="ResultCollector" testname="察看结果树" enabled="true">
            <boolProp name="ResultCollector.error_logging">false</boolProp>
            <objProp>
              <name>saveConfig</name>
              <value class="SampleSaveConfiguration">
                <time>true</time>
                <latency>true</latency>
                <timestamp>true</timestamp>
                <success>true</success>
                <label>true</label>
                <code>true</code>
                <message>true</message>
                <threadName>true</threadName>
                <dataType>true</dataType>
                <encoding>false</encoding>
                <assertions>true</assertions>
                <subresults>true</subresults>
                <responseData>false</responseData>
                <samplerData>false</samplerData>
                <xml>false</xml>
                <fieldNames>true</fieldNames>
                <responseHeaders>false</responseHeaders>
                <requestHeaders>false</requestHeaders>
                <responseDataOnError>false</responseDataOnError>
                <saveAssertionResultsFailureMessage>true</saveAssertionResultsFailureMessage>
                <assertionsResultsToSave>0</assertionsResultsToSave>
                <bytes>true</bytes>
                <sentBytes>true</sentBytes>
                <threadCounts>true</threadCounts>
                <idleTime>true</idleTime>
                <connectTime>true</connectTime>
              </value>
            </objProp>
            <stringProp name="filename"></stringProp>
          </ResultCollector>
          <hashTree/>
    '''
    return result_control_text


def result_polymerization_control():
    polymerization_text = '''
    <ResultCollector guiclass="StatVisualizer" testclass="ResultCollector" testname="聚合报告" enabled="true">
            <boolProp name="ResultCollector.error_logging">false</boolProp>
            <objProp>
              <name>saveConfig</name>
              <value class="SampleSaveConfiguration">
                <time>true</time>
                <latency>true</latency>
                <timestamp>true</timestamp>
                <success>true</success>
                <label>true</label>
                <code>true</code>
                <message>true</message>
                <threadName>true</threadName>
                <dataType>true</dataType>
                <encoding>false</encoding>
                <assertions>true</assertions>
                <subresults>true</subresults>
                <responseData>false</responseData>
                <samplerData>false</samplerData>
                <xml>false</xml>
                <fieldNames>true</fieldNames>
                <responseHeaders>false</responseHeaders>
                <requestHeaders>false</requestHeaders>
                <responseDataOnError>false</responseDataOnError>
                <saveAssertionResultsFailureMessage>true</saveAssertionResultsFailureMessage>
                <assertionsResultsToSave>0</assertionsResultsToSave>
                <bytes>true</bytes>
                <sentBytes>true</sentBytes>
                <threadCounts>true</threadCounts>
                <idleTime>true</idleTime>
                <connectTime>true</connectTime>
              </value>
            </objProp>
            <stringProp name="filename"></stringProp>
          </ResultCollector>
          <hashTree/>
    '''
    return polymerization_text


def requestid_bean_shell_control():
    shell_text = '''
    <BeanShellPreProcessor guiclass="TestBeanGUI" testclass="BeanShellPreProcessor" testname="BeanShell PreProcessor" enabled="true">
            <stringProp name="filename"></stringProp>
            <stringProp name="parameters"></stringProp>
            <boolProp name="resetInterpreter">false</boolProp>
            <stringProp name="script">import java.util.UUID;

 String uuid = UUID.randomUUID().toString();
        uuid = uuid.substring(0, 8)+uuid.substring(9,13)+uuid.substring(14,18)+uuid.substring(19,23)+uuid.substring(24);
        StringBuffer stringBuffer = new StringBuffer();
        for (int i=0;i&lt;uuid.length();i++){
            if (!Character.isDigit(uuid.charAt(i))){
                int value = uuid.charAt(i);
                stringBuffer.append(value);
                continue;
            }
            stringBuffer.append(uuid.charAt(i));
        }
   uuid = stringBuffer.toString().substring(5,14);     
vars.put(&quot;requestid&quot;, uuid);</stringProp>
          </BeanShellPreProcessor>
          <hashTree/>
    '''
    return shell_text


def cookie_control(cookies={}, url=''):
    default = '<hashTree/>'
    if cookies == {} or cookies is None:
        return default
    else:
        template_text = '''
         <elementProp name="{}" elementType="Cookie" testname="{}">
                <stringProp name="Cookie.value">{}</stringProp>
                <stringProp name="Cookie.domain">{}</stringProp>
                <stringProp name="Cookie.path">/</stringProp>
                <boolProp name="Cookie.secure">false</boolProp>
                <longProp name="Cookie.expires">0</longProp>
                <boolProp name="Cookie.path_specified">true</boolProp>
                <boolProp name="Cookie.domain_specified">true</boolProp>
              </elementProp>
        '''
        cookie_text = '''
        <CookieManager guiclass="CookiePanel" testclass="CookieManager" testname="HTTP Cookie 管理器" enabled="true">
            <collectionProp name="CookieManager.cookies">
            {}
            </collectionProp>
            <boolProp name="CookieManager.clearEachIteration">false</boolProp>
            <stringProp name="CookieManager.policy">standard</stringProp>
            <stringProp name="CookieManager.implementation">org.apache.jmeter.protocol.http.control.HC4CookieHandler</stringProp>
          </CookieManager>
        '''
        temp = ''
        for cookie in cookies:
            cookieKey = cookie['cookieKey']
            cookieValue = cookie['cookieValue']
            tem = template_text.format(cookieKey, cookieKey, cookieValue,
                                       url.split(r'://')[1].split(r'/')[0])
            temp += tem
        cookie_format_str = cookie_text.format(temp)
        return cookie_format_str + default


def header_control(header={}):
    default = '<hashTree/>'
    if header == [] or header is None:
        return default
    else:
        template_text = '''
         <elementProp name="" elementType="Header">
                <stringProp name="Header.name">{}</stringProp>
                <stringProp name="Header.value">{}</stringProp>
              </elementProp>
        '''
        head_text = '''
        <HeaderManager guiclass="HeaderPanel" testclass="HeaderManager" testname="HTTP信息头管理器" enabled="true">
            <collectionProp name="HeaderManager.headers">
              {}
            </collectionProp>
          </HeaderManager>
        '''
        temp = ''
        for head in header:
            headKey = head['headerKey']
            headValue = head['headerValue']
            tem = template_text.format(headKey, headValue)
            temp += tem
        header_format_str = head_text.format(temp)
        return header_format_str + default


def response_time_over_time(enable='true'):
    response_time_text = '''
    <kg.apc.jmeter.vizualizers.CorrectedResultCollector guiclass="kg.apc.jmeter.vizualizers.ResponseTimesOverTimeGui" testclass="kg.apc.jmeter.vizualizers.CorrectedResultCollector" testname="jp@gc - Response Times Over Time" enabled="{}">
            <boolProp name="ResultCollector.error_logging">false</boolProp>
            <objProp>
              <name>saveConfig</name>
              <value class="SampleSaveConfiguration">
                <time>true</time>
                <latency>true</latency>
                <timestamp>true</timestamp>
                <success>true</success>
                <label>true</label>
                <code>true</code>
                <message>true</message>
                <threadName>true</threadName>
                <dataType>true</dataType>
                <encoding>false</encoding>
                <assertions>true</assertions>
                <subresults>true</subresults>
                <responseData>false</responseData>
                <samplerData>false</samplerData>
                <xml>false</xml>
                <fieldNames>true</fieldNames>
                <responseHeaders>false</responseHeaders>
                <requestHeaders>false</requestHeaders>
                <responseDataOnError>false</responseDataOnError>
                <saveAssertionResultsFailureMessage>true</saveAssertionResultsFailureMessage>
                <assertionsResultsToSave>0</assertionsResultsToSave>
                <bytes>true</bytes>
                <sentBytes>true</sentBytes>
                <threadCounts>true</threadCounts>
                <idleTime>true</idleTime>
                <connectTime>true</connectTime>
              </value>
            </objProp>
            <stringProp name="filename"></stringProp>
            <longProp name="interval_grouping">500</longProp>
            <boolProp name="graph_aggregated">false</boolProp>
            <stringProp name="include_sample_labels"></stringProp>
            <stringProp name="exclude_sample_labels"></stringProp>
            <stringProp name="start_offset"></stringProp>
            <stringProp name="end_offset"></stringProp>
            <boolProp name="include_checkbox_state">false</boolProp>
            <boolProp name="exclude_checkbox_state">false</boolProp>
          </kg.apc.jmeter.vizualizers.CorrectedResultCollector>
          <hashTree/>
    '''.format(enable)
    return response_time_text


def transactions_per_second(enadble=True):
    transactions_per_text = '''
    <kg.apc.jmeter.vizualizers.CorrectedResultCollector guiclass="kg.apc.jmeter.vizualizers.TransactionsPerSecondGui" testclass="kg.apc.jmeter.vizualizers.CorrectedResultCollector" testname="jp@gc - Transactions per Second" enabled="{}">
            <boolProp name="ResultCollector.error_logging">false</boolProp>
            <objProp>
              <name>saveConfig</name>
              <value class="SampleSaveConfiguration">
                <time>true</time>
                <latency>true</latency>
                <timestamp>true</timestamp>
                <success>true</success>
                <label>true</label>
                <code>true</code>
                <message>true</message>
                <threadName>true</threadName>
                <dataType>true</dataType>
                <encoding>false</encoding>
                <assertions>true</assertions>
                <subresults>true</subresults>
                <responseData>false</responseData>
                <samplerData>false</samplerData>
                <xml>false</xml>
                <fieldNames>true</fieldNames>
                <responseHeaders>false</responseHeaders>
                <requestHeaders>false</requestHeaders>
                <responseDataOnError>false</responseDataOnError>
                <saveAssertionResultsFailureMessage>true</saveAssertionResultsFailureMessage>
                <assertionsResultsToSave>0</assertionsResultsToSave>
                <bytes>true</bytes>
                <sentBytes>true</sentBytes>
                <threadCounts>true</threadCounts>
                <idleTime>true</idleTime>
                <connectTime>true</connectTime>
              </value>
            </objProp>
            <stringProp name="filename"></stringProp>
            <longProp name="interval_grouping">1000</longProp>
            <boolProp name="graph_aggregated">false</boolProp>
            <stringProp name="include_sample_labels"></stringProp>
            <stringProp name="exclude_sample_labels"></stringProp>
            <stringProp name="start_offset"></stringProp>
            <stringProp name="end_offset"></stringProp>
            <boolProp name="include_checkbox_state">false</boolProp>
            <boolProp name="exclude_checkbox_state">false</boolProp>
          </kg.apc.jmeter.vizualizers.CorrectedResultCollector>
          <hashTree/>
    '''.format(str(enadble).lower())
    return transactions_per_text


def perfmon_metrics_collertor(ip='localhost', port=4444, enable=False):
    perfmon_metrics_text = '''
     <kg.apc.jmeter.perfmon.PerfMonCollector guiclass="kg.apc.jmeter.vizualizers.PerfMonGui" testclass="kg.apc.jmeter.perfmon.PerfMonCollector" testname="jp@gc - PerfMon Metrics Collector" enabled="{}">
            <boolProp name="ResultCollector.error_logging">false</boolProp>
            <objProp>
              <name>saveConfig</name>
              <value class="SampleSaveConfiguration">
                <time>true</time>
                <latency>true</latency>
                <timestamp>true</timestamp>
                <success>true</success>
                <label>true</label>
                <code>true</code>
                <message>true</message>
                <threadName>true</threadName>
                <dataType>true</dataType>
                <encoding>false</encoding>
                <assertions>true</assertions>
                <subresults>true</subresults>
                <responseData>false</responseData>
                <samplerData>false</samplerData>
                <xml>false</xml>
                <fieldNames>true</fieldNames>
                <responseHeaders>false</responseHeaders>
                <requestHeaders>false</requestHeaders>
                <responseDataOnError>false</responseDataOnError>
                <saveAssertionResultsFailureMessage>true</saveAssertionResultsFailureMessage>
                <assertionsResultsToSave>0</assertionsResultsToSave>
                <bytes>true</bytes>
                <sentBytes>true</sentBytes>
                <threadCounts>true</threadCounts>
                <idleTime>true</idleTime>
                <connectTime>true</connectTime>
              </value>
            </objProp>
            <stringProp name="filename"></stringProp>
            <longProp name="interval_grouping">1000</longProp>
            <boolProp name="graph_aggregated">false</boolProp>
            <stringProp name="include_sample_labels"></stringProp>
            <stringProp name="exclude_sample_labels"></stringProp>
            <stringProp name="start_offset"></stringProp>
            <stringProp name="end_offset"></stringProp>
            <boolProp name="include_checkbox_state">false</boolProp>
            <boolProp name="exclude_checkbox_state">false</boolProp>
            <collectionProp name="metricConnections">
              <collectionProp name="-456574074">
                <stringProp name="-1204607085">{}</stringProp>
                <stringProp name="1600768">{}</stringProp>
                <stringProp name="66952">CPU</stringProp>
                <stringProp name="0"></stringProp>
              </collectionProp>
              <collectionProp name="-2139682035">
                <stringProp name="-1204607085">{}</stringProp>
                <stringProp name="1600768">{}</stringProp>
                <stringProp name="-1993889503">Memory</stringProp>
                <stringProp name="0"></stringProp>
              </collectionProp>
              <collectionProp name="-373321737">
                <stringProp name="-1204607085">{}</stringProp>
                <stringProp name="1600768">{}</stringProp>
                <stringProp name="-274342153">Network I/O</stringProp>
                <stringProp name="0"></stringProp>
              </collectionProp>
              <collectionProp name="616642735">
                <stringProp name="-1204607085">{}</stringProp>
                <stringProp name="1600768">{}</stringProp>
                <stringProp name="2112896831">Disks I/O</stringProp>
                <stringProp name="0"></stringProp>
              </collectionProp>
            </collectionProp>
          </kg.apc.jmeter.perfmon.PerfMonCollector>
          <hashTree/>
    '''.format(str(enable).lower(), ip, port, ip, port, ip, port, ip, port)
    return perfmon_metrics_text


def jmx_end():
    end_text = '''
         </hashTree>
      </hashTree>
    </hashTree>
  </hashTree>
</jmeterTestPlan>
'''
    return end_text
