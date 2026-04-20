using System; 
using System.Collections.Generic; 
using System.Text; 
using H3; 

// ============================================
// 默认表单控制器（请勿修改或删除）
// 这个类名必须是表单编码，继承 SmartFormController
// ============================================
public class D287764133e46f8ed774cc3b4f0fe941c122f3c: H3.SmartForm.SmartFormController 
{ 
    public D287764133e46f8ed774cc3b4f0fe941c122f3c(H3.SmartForm.SmartFormRequest request): base(request) 
    { 
    } 

    protected override void OnLoad(H3.SmartForm.LoadSmartFormResponse response) 
    { 
        base.OnLoad(response); 
    } 

    protected override void OnSubmit(string actionName, H3.SmartForm.SmartFormPostValue postValue, H3.SmartForm.SubmitSmartFormResponse response) 
    { 
        base.OnSubmit(actionName, postValue, response); 
    } 
} 

// ============================================
// 测试接口（最简单的自定义接口）
// 用于验证自定义接口功能是否正常
// ============================================
public class TestApiController: H3.SmartForm.RestApiController 
{ 
    public TestApiController(H3.SmartForm.RestApiRequest request): base(request) { } 

    protected override void OnInvoke(string actionName, H3.SmartForm.RestApiResponse response) 
    { 
        // 无论传入什么 ActionName，都返回成功
        response.ReturnData.Add("result", "success");
        response.ReturnData.Add("message", "自定义接口测试成功");
        response.ReturnData.Add("receivedActionName", actionName);
    } 
}

// ============================================
// 字段映射接口（用于获取字段中文名）
// ============================================
public class FieldMappingApiController: H3.SmartForm.RestApiController 
{ 
    public FieldMappingApiController(H3.SmartForm.RestApiRequest request): base(request) { } 

    protected override void OnInvoke(string actionName, H3.SmartForm.RestApiResponse response) 
    { 
        if(actionName == "GetFieldMapping") 
        { 
            try
            {
                string targetSchema = this.Request.GetValue<string>("TargetSchema", ""); 
                
                if(string.IsNullOrEmpty(targetSchema))
                {
                    response.ReturnData.Add("result", "error");
                    response.ReturnData.Add("message", "TargetSchema 参数不能为空");
                    return;
                }
                
                H3.DataModel.BizObjectSchema schema = 
                    this.Request.Engine.BizObjectManager.GetPublishedSchema(targetSchema); 

                Dictionary<string, string> mapping = new Dictionary<string, string>(); 
                
                foreach(H3.DataModel.PropertySchema property in schema.Properties) 
                { 
                    if(!string.IsNullOrEmpty(property.DisplayName))
                    {
                        mapping.Add(property.Name, property.DisplayName); 
                    }
                } 

                response.ReturnData.Add("mapping", mapping); 
                response.ReturnData.Add("result", "success");
                response.ReturnData.Add("count", mapping.Count);
            }
            catch(Exception ex)
            {
                response.ReturnData.Add("result", "error");
                response.ReturnData.Add("message", ex.Message);
            }
        }
        else 
        { 
            response.ReturnData.Add("result", "error"); 
            response.ReturnData.Add("message", "未知的 ActionName: " + actionName); 
        } 
    } 
}
