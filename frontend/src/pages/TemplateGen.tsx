import { Input, Button, Typography, message, Divider } from 'antd'
import { useState } from 'react'
import AIModuleSelector from '../components/AIModuleSelector'
import { generateFromTemplate } from '../api/client'
import { useProjectStore } from '../store/useProjectStore'

export default function TemplateGen() {
  const [requirement, setRequirement] = useState('')
  const [loading, setLoading] = useState(false)
  const { selectedModules } = useProjectStore()

  const handleGenerate = async () => {
    if (!requirement.trim()) {
      message.warning('请输入项目需求描述')
      return
    }
    setLoading(true)
    try {
      const res = await generateFromTemplate(requirement, selectedModules)
      message.success(`已匹配模板：${res.data.template_used}，正在下载...`)
      window.location.href = `http://localhost:8000${res.data.download_url}`
    } catch {
      message.error('生成失败，请重试')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ padding: 32, maxWidth: 1000, margin: '0 auto' }}>
      <Typography.Title level={3}>从模板生成AI增强系统</Typography.Title>
      <Typography.Paragraph type="secondary">
        描述你需要的系统，平台将自动匹配最合适的模板（图书馆、商城、预约、宠物管理）
      </Typography.Paragraph>
      <Input.TextArea
        rows={4}
        placeholder="例如：图书馆管理系统，需要图书借阅、归还、查询功能，支持读者和管理员角色"
        value={requirement}
        onChange={(e) => setRequirement(e.target.value)}
        style={{ marginBottom: 24 }}
      />
      <Typography.Title level={4}>选择要注入的AI能力模块（可选）</Typography.Title>
      <AIModuleSelector />
      <Divider />
      <Button
        type="primary"
        size="large"
        loading={loading}
        onClick={handleGenerate}
        disabled={!requirement.trim()}
      >
        生成AI增强系统
      </Button>
    </div>
  )
}
