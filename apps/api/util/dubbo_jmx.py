def head_setting():
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


def run_crontrol_setting(pre_number, pre_time):
    run_crontrol_text = '''
    <hashTree>
      <ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="线程组" enabled="true">
        <stringProp name="ThreadGroup.on_sample_error">continue</stringProp>
        <elementProp name="ThreadGroup.main_controller" elementType="LoopController" guiclass="LoopControlPanel" testclass="LoopController" testname="循环控制器" enabled="true">
          <boolProp name="LoopController.continue_forever">false</boolProp>
          <intProp name="LoopController.loops">-1</intProp>
        </elementProp>
        <stringProp name="ThreadGroup.num_threads">{}</stringProp>
        <stringProp name="ThreadGroup.ramp_time">1</stringProp>
        <longProp name="ThreadGroup.start_time">1559613505000</longProp>
        <longProp name="ThreadGroup.end_time">1559613505000</longProp>
        <boolProp name="ThreadGroup.scheduler">true</boolProp>
        <stringProp name="ThreadGroup.duration">{}</stringProp>
        <stringProp name="ThreadGroup.delay"></stringProp>
      </ThreadGroup>
    '''.format(pre_number, pre_time)
    return run_crontrol_text


def dubbo_Sample_Gui_setting(ins_name,zkAddress, time_out, version, interface, method, paramType, paramValue):
    if paramValue.find('"') != -1:
        paramValue = paramValue.replace('"', '&quot;')
    dubbo_Sample_Gui_text = '''
    <hashTree>
        <io.github.ningyu.jmeter.plugin.dubbo.sample.DubboSample guiclass="io.github.ningyu.jmeter.plugin.dubbo.gui.DubboSampleGui" testclass="io.github.ningyu.jmeter.plugin.dubbo.sample.DubboSample" testname="{}" enabled="true">
          <stringProp name="FIELD_DUBBO_REGISTRY_PROTOCOL">zookeeper</stringProp>
          <stringProp name="FIELD_DUBBO_REGISTRY_GROUP"></stringProp>
          <stringProp name="FIELD_DUBBO_RPC_PROTOCOL">dubbo://</stringProp>
          <stringProp name="FIELD_DUBBO_ADDRESS">{}</stringProp>
          <stringProp name="FIELD_DUBBO_TIMEOUT">{}</stringProp>
          <stringProp name="FIELD_DUBBO_VERSION">{}</stringProp>
          <stringProp name="FIELD_DUBBO_RETRIES">0</stringProp>
          <stringProp name="FIELD_DUBBO_GROUP"></stringProp>
          <stringProp name="FIELD_DUBBO_CONNECTIONS">100</stringProp>
          <stringProp name="FIELD_DUBBO_LOADBALANCE">random</stringProp>
          <stringProp name="FIELD_DUBBO_ASYNC">sync</stringProp>
          <stringProp name="FIELD_DUBBO_CLUSTER">failfast</stringProp>
          <stringProp name="FIELD_DUBBO_INTERFACE">{}</stringProp>
          <stringProp name="FIELD_DUBBO_METHOD">{}</stringProp>
          <intProp name="FIELD_DUBBO_METHOD_ARGS_SIZE">1</intProp>
          <stringProp name="FIELD_DUBBO_METHOD_ARGS_PARAM_TYPE1">{}</stringProp>
          <stringProp name="FIELD_DUBBO_METHOD_ARGS_PARAM_VALUE1">{}</stringProp>
        </io.github.ningyu.jmeter.plugin.dubbo.sample.DubboSample>
    '''.format(ins_name,zkAddress, time_out, version, interface, method, paramType, paramValue)
    return dubbo_Sample_Gui_text


def watch_result_tree_setting():
    watch_result_text = '''
       <hashTree>
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
    return watch_result_text


def result_collector_setting():
    result_collector_text = '''
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
    return result_collector_text


def response_assertion_setting(assert_text):
    if assert_text.find('"') != -1:
        assert_text = assert_text.replace('"', '&quot;')
    response_assertion_text = '''
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
    return response_assertion_text


def response_TimesOver_TimeGui_setting():
    text = '''
        <kg.apc.jmeter.vizualizers.CorrectedResultCollector guiclass="kg.apc.jmeter.vizualizers.ResponseTimesOverTimeGui" testclass="kg.apc.jmeter.vizualizers.CorrectedResultCollector" testname="jp@gc - Response Times Over Time" enabled="true">
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
        '''
    return text


def transactions_PerSecond_Gui_setting():
    text = '''
        <kg.apc.jmeter.vizualizers.CorrectedResultCollector guiclass="kg.apc.jmeter.vizualizers.TransactionsPerSecondGui" testclass="kg.apc.jmeter.vizualizers.CorrectedResultCollector" testname="jp@gc - Transactions per Second" enabled="true">
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
        '''
    return text


def end_setting():
    text = '''
        </hashTree>
      </hashTree>
    </hashTree>
  </hashTree>
</jmeterTestPlan>
        '''
    return text
