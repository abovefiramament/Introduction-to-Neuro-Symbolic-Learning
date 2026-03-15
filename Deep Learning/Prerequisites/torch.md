## 一、核心组件关系总览

先理清组件间的依赖逻辑，所有流程都围绕这个闭环展开：











预览

查看代码

<svg aria-roledescription="flowchart-v2" role="graphics-document document" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/2000/svg" width="100%" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:ev="http://www.w3.org/2001/xml-events"><g transform="matrix(0.5885093167701864,0,0,0.5885093167701864,318.0390210122055,0)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><g style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><marker orient="auto" markerHeight="8" markerWidth="8" markerUnits="userSpaceOnUse" refY="5" refX="5" viewBox="0 0 10 10" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><path style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" d="M 0 0 L 10 5 L 0 10 z"></path></marker><marker orient="auto" markerHeight="8" markerWidth="8" markerUnits="userSpaceOnUse" refY="5" refX="4.5" viewBox="0 0 10 10" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><path style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" d="M 0 5 L 10 10 L 10 0 z"></path></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5" refX="11" viewBox="0 0 10 10" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><circle style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" r="5" cy="5" cx="5"></circle></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5" refX="-1" viewBox="0 0 10 10" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><circle style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" r="5" cy="5" cx="5"></circle></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5.2" refX="12" viewBox="0 0 11 11" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><path style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" d="M 1,1 l 9,9 M 10,1 l -9,9"></path></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5.2" refX="-1" viewBox="0 0 11 11" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><path style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" d="M 1,1 l 9,9 M 10,1 l -9,9"></path></marker><g style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><g style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></g><g style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><path marker-end="url(#svg-mermaid-diagram-shiyva4_flowchart-v2-pointEnd)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" d="M142.5,74L142.5,78.167C142.5,82.333,142.5,90.667,142.5,98.333C142.5,106,142.5,113,142.5,116.5L142.5,120"></path><path marker-end="url(#svg-mermaid-diagram-shiyva4_flowchart-v2-pointEnd)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" d="M142.5,190L142.5,194.167C142.5,198.333,142.5,206.667,142.5,214.333C142.5,222,142.5,229,142.5,232.5L142.5,236"></path><path marker-end="url(#svg-mermaid-diagram-shiyva4_flowchart-v2-pointEnd)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" d="M114.827,288L110.022,292.167C105.218,296.333,95.609,304.667,90.804,312.333C86,320,86,327,86,330.5L86,334"></path><path marker-end="url(#svg-mermaid-diagram-shiyva4_flowchart-v2-pointEnd)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" d="M86,404L86,408.167C86,412.333,86,420.667,86,428.333C86,436,86,443,86,446.5L86,450"></path><path marker-end="url(#svg-mermaid-diagram-shiyva4_flowchart-v2-pointEnd)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" d="M86,520L86,524.167C86,528.333,86,536.667,89.594,544.522C93.187,552.378,100.375,559.757,103.969,563.446L107.562,567.135"></path><path marker-end="url(#svg-mermaid-diagram-shiyva4_flowchart-v2-pointEnd)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" d="M174.647,570L178.705,565.833C182.764,561.667,190.882,553.333,194.941,539.5C199,525.667,199,506.333,199,487C199,467.667,199,448.333,199,429C199,409.667,199,390.333,199,371C199,351.667,199,332.333,194.699,318.937C190.398,305.54,181.797,298.08,177.496,294.351L173.195,290.621"></path></g><g style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><g style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><g transform="translate(0, 0)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><foreignObject height="0" width="0" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></span></div></foreignObject></g></g><g style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><g transform="translate(0, 0)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><foreignObject height="0" width="0" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></span></div></foreignObject></g></g><g style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><g transform="translate(0, 0)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><foreignObject height="0" width="0" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></span></div></foreignObject></g></g><g style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><g transform="translate(0, 0)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><foreignObject height="0" width="0" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></span></div></foreignObject></g></g><g style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><g transform="translate(0, 0)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><foreignObject height="0" width="0" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></span></div></foreignObject></g></g><g style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><g transform="translate(0, 0)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><foreignObject height="0" width="0" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></span></div></foreignObject></g></g></g><g style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><g transform="translate(142.5, 41)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect height="66" width="174.30208587646484" y="-33" x="-87.15104293823242" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><g transform="translate(-57.15104293823242, -18)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><foreignObject height="36" width="114.30208587646484" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><p style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">自定义Dataset<br style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">（数据读取/预处理）</p></span></div></foreignObject></g></g><g transform="translate(142.5, 157)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect height="66" width="198.30209350585938" y="-33" x="-99.15104675292969" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><g transform="translate(-69.15104675292969, -18)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><foreignObject height="36" width="138.30209350585938" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><p style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">DataLoader<br style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">（批次生成/多进程加载）</p></span></div></foreignObject></g></g><g transform="translate(142.5, 264)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect height="48" width="132" y="-24" x="-66" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><g transform="translate(-36, -9)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><foreignObject height="18" width="72" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><p style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">模型参数更新</p></span></div></foreignObject></g></g><g transform="translate(86, 371)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect height="66" width="156" y="-33" x="-78" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><g transform="translate(-48, -18)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><foreignObject height="36" width="96" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><p style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">损失函数<br style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">（计算预测误差）</p></span></div></foreignObject></g></g><g transform="translate(86, 487)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect height="66" width="156" y="-33" x="-78" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><g transform="translate(-48, -18)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><foreignObject height="36" width="96" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><p style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">优化器<br style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">（更新模型参数）</p></span></div></foreignObject></g></g><g transform="translate(142.5, 603)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect height="66" width="145.0625" y="-33" x="-72.53125" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><g transform="translate(-42.53125, -18)" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><foreignObject height="36" width="85.0625" style="color: rgb(28, 31, 35); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><p style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">学习率调度器<br style="color: rgb(28, 31, 35); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">（动态调整LR）</p></span></div></foreignObject></g></g></g></g></g></g></svg>

```
graph TD
    A[自定义Dataset<br>（数据读取/预处理）] --> B[DataLoader<br>（批次生成/多进程加载）]
    B --> C[自定义Model<br>（模型前向传播）]
    C --> D[损失函数<br>（计算预测误差）]
    D --> E[优化器<br>（更新模型参数）]
    E --> F[学习率调度器<br>（动态调整LR）]
    F --> C[模型参数更新]
```

<svg aria-roledescription="flowchart-v2" role="graphics-document document" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/2000/svg" width="100%" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:ev="http://www.w3.org/2001/xml-events"><g transform="matrix(1.4518633540372672,0,0,1.4518633540372672,668.2704080380267,-5.684341886080802e-14)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><g style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><marker orient="auto" markerHeight="8" markerWidth="8" markerUnits="userSpaceOnUse" refY="5" refX="5" viewBox="0 0 10 10" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><path style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" d="M 0 0 L 10 5 L 0 10 z"></path></marker><marker orient="auto" markerHeight="8" markerWidth="8" markerUnits="userSpaceOnUse" refY="5" refX="4.5" viewBox="0 0 10 10" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><path style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" d="M 0 5 L 10 10 L 10 0 z"></path></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5" refX="11" viewBox="0 0 10 10" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><circle style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" r="5" cy="5" cx="5"></circle></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5" refX="-1" viewBox="0 0 10 10" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><circle style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" r="5" cy="5" cx="5"></circle></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5.2" refX="12" viewBox="0 0 11 11" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><path style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" d="M 1,1 l 9,9 M 10,1 l -9,9"></path></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5.2" refX="-1" viewBox="0 0 11 11" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><path style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" d="M 1,1 l 9,9 M 10,1 l -9,9"></path></marker><g style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><g style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></g><g style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><path marker-end="url(#svg-mermaid-diagram-h6c23go_flowchart-v2-pointEnd)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" d="M142.5,74L142.5,78.167C142.5,82.333,142.5,90.667,142.5,98.333C142.5,106,142.5,113,142.5,116.5L142.5,120"></path><path marker-end="url(#svg-mermaid-diagram-h6c23go_flowchart-v2-pointEnd)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" d="M142.5,190L142.5,194.167C142.5,198.333,142.5,206.667,142.5,214.333C142.5,222,142.5,229,142.5,232.5L142.5,236"></path><path marker-end="url(#svg-mermaid-diagram-h6c23go_flowchart-v2-pointEnd)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" d="M114.827,288L110.022,292.167C105.218,296.333,95.609,304.667,90.804,312.333C86,320,86,327,86,330.5L86,334"></path><path marker-end="url(#svg-mermaid-diagram-h6c23go_flowchart-v2-pointEnd)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" d="M86,404L86,408.167C86,412.333,86,420.667,86,428.333C86,436,86,443,86,446.5L86,450"></path><path marker-end="url(#svg-mermaid-diagram-h6c23go_flowchart-v2-pointEnd)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" d="M86,520L86,524.167C86,528.333,86,536.667,89.594,544.522C93.187,552.378,100.375,559.757,103.969,563.446L107.562,567.135"></path><path marker-end="url(#svg-mermaid-diagram-h6c23go_flowchart-v2-pointEnd)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" d="M174.647,570L178.705,565.833C182.764,561.667,190.882,553.333,194.941,539.5C199,525.667,199,506.333,199,487C199,467.667,199,448.333,199,429C199,409.667,199,390.333,199,371C199,351.667,199,332.333,194.699,318.937C190.398,305.54,181.797,298.08,177.496,294.351L173.195,290.621"></path></g><g style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><g style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><g transform="translate(0, 0)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><foreignObject height="0" width="0" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></span></div></foreignObject></g></g><g style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><g transform="translate(0, 0)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><foreignObject height="0" width="0" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></span></div></foreignObject></g></g><g style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><g transform="translate(0, 0)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><foreignObject height="0" width="0" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></span></div></foreignObject></g></g><g style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><g transform="translate(0, 0)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><foreignObject height="0" width="0" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></span></div></foreignObject></g></g><g style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><g transform="translate(0, 0)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><foreignObject height="0" width="0" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></span></div></foreignObject></g></g><g style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><g transform="translate(0, 0)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><foreignObject height="0" width="0" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></span></div></foreignObject></g></g></g><g style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><g transform="translate(142.5, 41)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect height="66" width="174.30208587646484" y="-33" x="-87.15104293823242" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><g transform="translate(-57.15104293823242, -18)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><foreignObject height="36" width="114.30208587646484" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><p style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">自定义Dataset<br style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">（数据读取/预处理）</p></span></div></foreignObject></g></g><g transform="translate(142.5, 157)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect height="66" width="198.30209350585938" y="-33" x="-99.15104675292969" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><g transform="translate(-69.15104675292969, -18)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><foreignObject height="36" width="138.30209350585938" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><p style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">DataLoader<br style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">（批次生成/多进程加载）</p></span></div></foreignObject></g></g><g transform="translate(142.5, 264)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect height="48" width="132" y="-24" x="-66" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><g transform="translate(-36, -9)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><foreignObject height="18" width="72" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><p style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">模型参数更新</p></span></div></foreignObject></g></g><g transform="translate(86, 371)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect height="66" width="156" y="-33" x="-78" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><g transform="translate(-48, -18)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><foreignObject height="36" width="96" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><p style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">损失函数<br style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">（计算预测误差）</p></span></div></foreignObject></g></g><g transform="translate(86, 487)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect height="66" width="156" y="-33" x="-78" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><g transform="translate(-48, -18)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><foreignObject height="36" width="96" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><p style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">优化器<br style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">（更新模型参数）</p></span></div></foreignObject></g></g><g transform="translate(142.5, 603)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect height="66" width="145.0625" y="-33" x="-72.53125" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><g transform="translate(-42.53125, -18)" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><rect style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"></rect><foreignObject height="36" width="85.0625" style="color: rgb(0, 0, 0); font: 12px / 24px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 24px; text-align: start; white-space: normal; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><div style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: table-cell; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);" xmlns="http://www.w3.org/1999/xhtml"><span style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);"><p style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: block; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">学习率调度器<br style="color: rgb(0, 0, 0); font: 12px / 18px &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 12px; font-weight: 400; line-height: 18px; text-align: center; white-space: nowrap; display: inline; flex: 0 1 auto; flex-direction: row; justify-content: normal; align-items: normal; padding: 0px; margin: 0px; background: rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box; background-color: rgba(0, 0, 0, 0);">（动态调整LR）</p></span></div></foreignObject></g></g></g></g></g></g></svg>

![image-20260312153748633](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20260312153748633.png)

------

## 二、核心组件 1：模型搭建（`torch.nn.Module`）

### 1. 核心定位

`nn.Module` 是 PyTorch 所有模型的「基类」，负责：

- 管理模型参数（自动注册可训练参数）；
- 实现前向传播逻辑（`forward` 方法）；
- 支持设备迁移（`.to()`）、多卡并行（`DataParallel`）、参数保存 / 加载（`.state_dict()`）。

### 2. 基础用法（以 LLM 核心模块为例）

#### 步骤 1：自定义模型类（继承 `nn.Module`）

python



运行









```
import torch
import torch.nn as nn
import torch.nn.functional as F

# 示例：LLM 中的单个 Transformer Decoder 层（简化版）
class DecoderLayer(nn.Module):
    def __init__(self, dim, n_heads):
        super().__init__()  # 必须调用父类初始化
        self.self_attn = nn.MultiheadAttention(dim, n_heads, batch_first=True)
        self.ffn = nn.Sequential(
            nn.Linear(dim, 4*dim),
            nn.GELU(),
            nn.Linear(4*dim, dim)
        )
        self.norm1 = nn.LayerNorm(dim)
        self.norm2 = nn.LayerNorm(dim)

    # 核心：实现前向传播逻辑
    def forward(self, x, mask=None):
        # 自注意力 + 残差连接 + 层归一化
        x = x + self.self_attn(self.norm1(x), self.norm1(x), self.norm1(x), attn_mask=mask)[0]
        # 前馈网络 + 残差连接 + 层归一化
        x = x + self.ffn(self.norm2(x))
        return x

# 示例：完整的 Tiny-K 模型
class TinyKModel(nn.Module):
    def __init__(self, dim=768, n_layers=12, n_heads=12, vocab_size=6144, max_seq_len=512):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, dim)  # 词嵌入层
        self.layers = nn.ModuleList([DecoderLayer(dim, n_heads) for _ in range(n_layers)])  # 堆叠Decoder层
        self.lm_head = nn.Linear(dim, vocab_size)  # 输出层（LM Head）
        self.max_seq_len = max_seq_len

    def forward(self, input_ids, labels=None):
        # 1. 词嵌入
        x = self.embedding(input_ids)  # [batch, seq_len, dim]
        
        # 2. 生成因果掩码（防止看到未来token）
        causal_mask = torch.tril(torch.ones((self.max_seq_len, self.max_seq_len), device=input_ids.device))
        causal_mask = causal_mask.masked_fill(causal_mask == 0, float('-inf'))
        causal_mask = causal_mask.masked_fill(causal_mask == 1, 0.0)

        # 3. 逐层前向传播
        for layer in self.layers:
            x = layer(x, mask=causal_mask[:input_ids.shape[1], :input_ids.shape[1]])
        
        # 4. LM Head 输出logits
        logits = self.lm_head(x)  # [batch, seq_len, vocab_size]

        # 5. 计算损失（自回归语言建模）
        loss = None
        if labels is not None:
            # 交叉熵损失：flatten后计算（适配batch+seq_len）
            loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)), labels.reshape(-1), ignore_index=0)
        
        return logits, loss
```

#### 步骤 2：模型初始化与基本操作

python



运行









```
# 1. 实例化模型
model = TinyKModel(dim=768, n_layers=12, n_heads=12, vocab_size=6144)

# 2. 设备迁移（GPU/CPU）
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# 3. 查看模型参数
print(f"总参数量：{sum(p.numel() for p in model.parameters()) / 1e6:.2f}M")

# 4. 前向传播测试
batch_input = torch.randint(0, 6144, (2, 512)).to(device)  # [batch=2, seq_len=512]
logits, loss = model(batch_input, labels=batch_input)
print(f"Logits形状：{logits.shape}, 损失值：{loss.item():.4f}")

# 5. 保存/加载模型
# 保存参数
torch.save(model.state_dict(), "tiny_k_model.pth")
# 加载参数
model.load_state_dict(torch.load("tiny_k_model.pth", map_location=device))
```

### 3. 进阶技巧（LLM 场景必备）

1. 参数冻结

   ：微调时冻结底层层，只训练顶层

   python

   

   运行

   

   

   

   

   ```
   # 冻结前8层Decoder
   for i, layer in enumerate(model.layers):
       if i < 8:
           for param in layer.parameters():
               param.requires_grad = False
   ```

   

2. 多卡并行

   ：单机多卡训练

   python

   

   运行

   

   

   

   

   ```
   if torch.cuda.device_count() > 1:
       model = nn.DataParallel(model)  # 自动拆分批次到多卡
   ```

   

3. 推理模式

   ：禁用梯度计算，节省显存

   python

   

   运行

   

   

   

   

   ```
   model.eval()  # 切换到评估模式（禁用Dropout/BatchNorm）
   with torch.inference_mode():  # 比torch.no_grad()更高效
       logits, _ = model(batch_input)
   ```

   

### 4. 常见坑

- ❌ 忘记调用 `super().__init__()`：会导致参数无法注册，优化器找不到参数；
- ❌ `forward` 方法里写硬编码的设备：比如 `x = x.to("cuda:0")`，多卡训练时会报错；
- ❌ 直接修改 `nn.Module` 内的张量：比如 `self.x = torch.zeros(10)`，需用 `nn.Parameter` 包装才能被优化器识别。

------

## 三、核心组件 2：Dataset & DataLoader

### 1. 核心定位

- **Dataset**：自定义数据读取逻辑（继承 `torch.utils.data.Dataset`），实现「懒加载」和「样本预处理」；
- **DataLoader**：封装 Dataset，实现「批次生成」「多进程加载」「数据打乱」，解决 GPU 饥饿问题。

### 2. 基础用法（结合你的 PretrainDataset）

#### 步骤 1：自定义 Dataset（你之前写的简化版）

python



运行









```
from torch.utils.data import Dataset, DataLoader
import json
import numpy as np

class PretrainDataset(Dataset):
    def __init__(self, data_path, tokenizer, max_length=512):
        super().__init__()
        self.data_path = data_path
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.pad_token_id = tokenizer.pad_token_id or 0
        
        # 预计算每行字节偏移量（O(1)随机访问）
        self._offsets = []
        with open(data_path, 'rb') as f:
            self._offsets.append(0)
            while f.readline():
                self._offsets.append(f.tell())
        self._total_lines = len(self._offsets) - 1

    # 必须实现：返回总样本数
    def __len__(self):
        return self._total_lines

    # 必须实现：根据索引返回单样本
    def __getitem__(self, index):
        # 1. 读取单条数据
        with open(self.data_path, 'rb') as f:
            f.seek(self._offsets[index])
            line = f.readline().decode('utf-8')
        sample = json.loads(line)
        text = self.tokenizer.bos_token + sample['text']
        
        # 2. 分词+截断+填充
        input_ids = self.tokenizer(text)['input_ids'][:self.max_length]
        text_len = len(input_ids)
        input_ids = input_ids + [self.pad_token_id] * (self.max_length - text_len)
        
        # 3. 构造自回归样本（X=input_ids[:-1], Y=input_ids[1:]）
        loss_mask = [1]*text_len + [0]*(self.max_length - text_len)  # padding部分不计算损失
        input_ids = np.array(input_ids, dtype=np.int64)
        X = input_ids[:-1]
        Y = input_ids[1:]
        loss_mask = np.array(loss_mask[1:], dtype=np.int64)
        
        return torch.from_numpy(X), torch.from_numpy(Y), torch.from_numpy(loss_mask)
```

#### 步骤 2：封装 DataLoader

python



运行









```
from transformers import AutoTokenizer

# 加载分词器
tokenizer = AutoTokenizer.from_pretrained("./tokenizer_k/")
tokenizer.pad_token = tokenizer.eos_token

# 初始化Dataset
train_ds = PretrainDataset(
    data_path="./pretrain_data.jsonl",
    tokenizer=tokenizer,
    max_length=512
)

# 初始化DataLoader（核心参数详解）
train_loader = DataLoader(
    dataset=train_ds,
    batch_size=8,  # 批次大小（根据GPU显存调整）
    shuffle=True,  # 训练时打乱数据（验证集设为False）
    num_workers=8,  # 多进程加载数据（CPU核心数的1-2倍）
    pin_memory=True,  # 锁定内存，加速GPU数据传输
    drop_last=False,  # 是否丢弃最后一个不完整批次（训练集可设为True）
    prefetch_factor=2  # 预取批次数，提前准备下一批数据
)

# 遍历DataLoader
for step, (X, Y, loss_mask) in enumerate(train_loader):
    print(f"Step {step}: X形状={X.shape}, Y形状={Y.shape}, loss_mask形状={loss_mask.shape}")
    # X.shape: [8, 511], Y.shape: [8, 511], loss_mask.shape: [8, 511]
    break
```

### 3. 进阶技巧（LLM 场景必备）

1. 自定义 Collate_fn

   ：处理变长序列（替代固定长度填充）

   python

   

   运行

   

   

   

   

   ```
   def collate_fn(batch):
       # batch是列表，每个元素是(X,Y,loss_mask)
       X = [item[0] for item in batch]
       Y = [item[1] for item in batch]
       loss_mask = [item[2] for item in batch]
       # 动态填充到批次内最长长度
       X = nn.utils.rnn.pad_sequence(X, batch_first=True, padding_value=0)
       Y = nn.utils.rnn.pad_sequence(Y, batch_first=True, padding_value=0)
       loss_mask = nn.utils.rnn.pad_sequence(loss_mask, batch_first=True, padding_value=0)
       return X, Y, loss_mask
   
   # DataLoader中指定collate_fn
   train_loader = DataLoader(train_ds, batch_size=8, collate_fn=collate_fn, ...)
   ```

   

2. 流式加载

   ：处理超大语料（无需全量加载）

   python

   

   运行

   

   

   

   

   ```
   from torch.utils.data import IterableDataset
   class StreamingDataset(IterableDataset):
       def __init__(self, data_path):
           self.data_path = data_path
       def __iter__(self):
           with open(self.data_path, 'r', encoding='utf-8') as f:
               for line in f:
                   yield json.loads(line)['text']
   ```

   

### 4. 常见坑

- ❌ `num_workers` 设置过大：导致 CPU 过载，反而变慢（建议≤CPU 核心数）；
- ❌ 多进程加载时用全局变量：会导致数据重复加载，需把数据路径传入 Dataset；
- ❌ `pin_memory=True` 用在 CPU 训练：无意义，还会浪费内存。

------

## 四、核心组件 3：损失函数

### 1. 核心定位

损失函数是「模型优化的目标」，衡量模型预测值与真实标签的差距，LLM 预训练核心用 **交叉熵损失（CrossEntropyLoss）**。

### 2. 基础用法（适配 LLM 自回归场景）

#### 场景 1：基础交叉熵损失（处理 padding）

python



运行









```
# 1. 定义损失函数（ignore_index忽略padding token）
criterion = nn.CrossEntropyLoss(ignore_index=0)  # 0是pad_token_id

# 2. 模拟模型输出和标签
batch_size, seq_len, vocab_size = 2, 511, 6144
logits = torch.randn(batch_size, seq_len, vocab_size)  # 模型输出
labels = torch.randint(0, vocab_size, (batch_size, seq_len))  # 真实标签
labels[0, 500:] = 0  # 模拟padding部分

# 3. 计算损失（需flatten logits和labels）
loss = criterion(logits.reshape(-1, vocab_size), labels.reshape(-1))
print(f"基础损失值：{loss.item():.4f}")
```

#### 场景 2：带损失掩码的损失计算（你之前的逻辑）

python



运行









```
# 模拟loss_mask（1=计算损失，0=忽略）
loss_mask = torch.ones_like(labels)
loss_mask[0, 500:] = 0  # padding部分设为0

# 计算有效损失（只对非padding部分求和）
loss = criterion(logits.reshape(-1, vocab_size), labels.reshape(-1))
loss_mask_flat = loss_mask.reshape(-1)
loss = torch.sum(loss * loss_mask_flat) / loss_mask_flat.sum()
print(f"带掩码损失值：{loss.item():.4f}")
```

### 3. 常用损失函数（适配不同场景）

表格







|       损失函数        |         适用场景         |                          关键参数                          |
| :-------------------: | :----------------------: | :--------------------------------------------------------: |
| `nn.CrossEntropyLoss` |  LLM 预训练 / 分类任务   | `ignore_index`（忽略 padding）、`reduction`（求和 / 平均） |
|     `nn.MSELoss`      |  回归任务（如评分预测）  |                        `reduction`                         |
|     `nn.BCELoss`      | 二分类任务（如文本分类） |                    `weight`（类别权重）                    |
|     `nn.NLLLoss`      |  对数概率输出的分类任务  |                       `ignore_index`                       |

### 4. 常见坑

- ❌ 未 flatten logits 和 labels：CrossEntropyLoss 要求输入是 `[N, C]`，标签是 `[N]`，直接传 `[batch, seq_len, C]` 会报错；
- ❌ 忽略 `ignore_index`：padding 部分参与损失计算，导致模型学习无意义的 padding token；
- ❌ `reduction="mean"` 直接用：padding 部分会拉低损失值，需先掩码再手动平均。

------

## 五、核心组件 4：优化器 & 学习率调度器

### 1. 核心定位

- **优化器**：根据损失的梯度更新模型参数（如 AdamW）；
- **学习率调度器**：动态调整学习率（如 Warmup + 余弦退火），让模型更稳定收敛。

### 2. 基础用法（LLM 预训练标配）

#### 步骤 1：定义优化器（AdamW 是 LLM 首选）

python



运行









```
# 1. 定义优化器（核心参数：lr=学习率，weight_decay=权重衰减）
optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=2e-4,  # 初始学习率（LLM预训练常用1e-4~5e-4）
    weight_decay=0.01,  # 权重衰减（防止过拟合）
    betas=(0.9, 0.999)  # 动量参数（默认即可）
)

# 2. 查看优化器参数组
print(f"优化器参数组数量：{len(optimizer.param_groups)}")
print(f"初始学习率：{optimizer.param_groups[0]['lr']}")
```

#### 步骤 2：自定义学习率调度器（你之前的 get_lr 逻辑）

python



运行









```
import math

def get_lr(it, total_iters, warmup_iters=1000, base_lr=2e-4, min_lr=2e-5):
    # Warmup阶段：线性增长
    if it < warmup_iters:
        return base_lr * it / warmup_iters
    # 余弦退火阶段：线性衰减到最小学习率
    if it > total_iters:
        return min_lr
    decay_ratio = (it - warmup_iters) / (total_iters - warmup_iters)
    coeff = 0.5 * (1 + math.cos(math.pi * decay_ratio))
    return min_lr + coeff * (base_lr - min_lr)

# 训练循环中动态调整学习率
total_iters = len(train_loader) * 10  # 总迭代步数（10个epoch）
for step, (X, Y, loss_mask) in enumerate(train_loader):
    # 1. 动态更新学习率
    lr = get_lr(step, total_iters)
    for param_group in optimizer.param_groups:
        param_group['lr'] = lr
    
    # 2. 前向传播+计算损失
    logits, loss = model(X.to(device), Y.to(device))
    loss_mask = loss_mask.to(device)
    loss = torch.sum(loss * loss_mask) / loss_mask.sum()
    
    # 3. 反向传播+更新参数
    optimizer.zero_grad()  # 清零梯度
    loss.backward()  # 反向传播计算梯度
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)  # 梯度裁剪
    optimizer.step()  # 更新参数
    
    if step % 100 == 0:
        print(f"Step {step}: LR={lr:.7f}, Loss={loss.item():.4f}")
    break
```

#### 步骤 3：PyTorch 内置调度器（简化版）

python



运行









```
# 示例：余弦退火调度器
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
    optimizer,
    T_max=len(train_loader)*10,  # 余弦周期
    eta_min=2e-5  # 最小学习率
)

# 训练循环中更新
for step, (X, Y, loss_mask) in enumerate(train_loader):
    # ... 前向传播+反向传播 ...
    optimizer.step()
    scheduler.step()  # 每步更新学习率
```

### 3. 进阶技巧（LLM 场景必备）

1. 梯度累积

   ：模拟大批次（显存不够时用）

   python

   

   运行

   

   

   

   

   ```
   accumulation_steps = 8  # 累积8步更新一次
   for step, (X, Y, loss_mask) in enumerate(train_loader):
       # 前向传播+损失计算（除以累积步数）
       loss = loss / accumulation_steps
       loss.backward()
       
       # 每accumulation_steps步更新一次
       if (step + 1) % accumulation_steps == 0:
           torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
           optimizer.step()
           optimizer.zero_grad()
   ```

   

2. 混合精度训练

   ：减少显存占用

   python

   

   运行

   

   

   

   

   ```
   scaler = torch.cuda.amp.GradScaler()  # 梯度缩放器
   for step, (X, Y, loss_mask) in enumerate(train_loader):
       with torch.cuda.amp.autocast():  # 混合精度上下文
           logits, loss = model(X.to(device), Y.to(device))
       
       scaler.scale(loss).backward()  # 缩放梯度
       scaler.step(optimizer)  # 更新参数
       scaler.update()  # 更新缩放器
       optimizer.zero_grad()
   ```

   

### 4. 常见坑

- ❌ 忘记调用 `optimizer.zero_grad()`：梯度累积，导致参数更新错误；

- ❌ 权重衰减应用到偏置 / 嵌入层：需单独设置参数组，避免偏置层衰减；

  python

  

  运行

  

  

  

  

  ```
  # 分开设置参数组（偏置/嵌入层不衰减）
  no_decay = ["bias", "LayerNorm.weight", "embedding.weight"]
  optimizer_grouped_parameters = [
      {
          "params": [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)],
          "weight_decay": 0.01,
      },
      {
          "params": [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)],
          "weight_decay": 0.0,
      },
  ]
  optimizer = AdamW(optimizer_grouped_parameters, lr=2e-4)
  ```

  

- ❌ 学习率调度器更新时机错误：应在 `optimizer.step()` 之后调用。

------

## 六、核心组件 5：训练循环（串联所有组件）

### 完整训练循环示例（LLM 预训练标配）

python



运行









```
import time

# 初始化所有组件
model = TinyKModel().to(device)
train_ds = PretrainDataset("./pretrain_data.jsonl", tokenizer)
train_loader = DataLoader(train_ds, batch_size=8, shuffle=True, num_workers=8)
optimizer = AdamW(model.parameters(), lr=2e-4, weight_decay=0.01)
scaler = torch.cuda.amp.GradScaler()
accumulation_steps = 8
epochs = 10

# 训练循环
model.train()  # 训练模式（启用Dropout）
for epoch in range(epochs):
    start_time = time.time()
    total_loss = 0.0
    
    for step, (X, Y, loss_mask) in enumerate(train_loader):
        # 1. 数据迁移
        X, Y, loss_mask = X.to(device), Y.to(device), loss_mask.to(device)
        
        # 2. 动态调整学习率
        lr = get_lr(epoch*len(train_loader)+step, epochs*len(train_loader))
        for param_group in optimizer.param_groups:
            param_group['lr'] = lr
        
        # 3. 混合精度前向传播
        with torch.cuda.amp.autocast():
            logits, loss = model(X, Y)
            loss_mask = loss_mask.reshape(-1)
            loss = torch.sum(loss * loss_mask) / loss_mask.sum()
            loss = loss / accumulation_steps  # 梯度累积
        
        # 4. 反向传播
        scaler.scale(loss).backward()
        
        # 5. 梯度累积+更新参数
        if (step + 1) % accumulation_steps == 0:
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            scaler.step(optimizer)
            scaler.update()
            optimizer.zero_grad(set_to_none=True)
        
        # 6. 日志记录
        total_loss += loss.item() * accumulation_steps
        if step % 100 == 0:
            avg_loss = total_loss / (step + 1)
            spend_time = time.time() - start_time
            print(f"Epoch {epoch+1}/{epochs}, Step {step}, Loss {avg_loss:.4f}, LR {lr:.7f}, Time {spend_time:.2f}s")
    
    # 7. 保存模型
    torch.save(model.state_dict(), f"tiny_k_epoch_{epoch+1}.pth")
    print(f"Epoch {epoch+1} finished, avg loss: {total_loss/len(train_loader):.4f}")
```

------

## 七、总结（核心知识点回顾）

1. **模型搭建**：继承 `nn.Module`，实现 `forward` 方法，用 `nn.Parameter` 包装可训练参数，多卡训练用 `DataParallel`；
2. **Dataset & DataLoader**：Dataset 实现 `__len__`/`__getitem__`，DataLoader 控制批次 / 多进程，LLM 场景用「字节偏移量 + 懒加载」处理大语料；
3. **损失函数**：LLM 预训练用 `CrossEntropyLoss`，必须处理 padding（`ignore_index` 或损失掩码），避免无意义损失；
4. **优化器 & 调度器**：AdamW 是 LLM 首选，配合 Warmup + 余弦退火调度器，梯度累积 / 混合精度 / 梯度裁剪是显存优化三板斧；
5. **训练循环**：核心闭环是「数据加载→前向传播→损失计算→反向传播→参数更新」，日志 / 保存 / 动态 LR 是工程化必备。