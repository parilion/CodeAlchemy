import { Button, Divider, Typography, message, Alert } from 'antd'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import AIModuleSelector from '../components/AIModuleSelector'
import { enhanceProject } from '../api/client'
import { useProjectStore } from '../store/useProjectStore'

export default function ConfigureAI() {
  const { currentProjectId, selectedModules } = useProjectStore()
  const [loading, setLoading] = useState(false)
  const nav = useNavigate()

  const handleEnhance = async () => {
    if (!currentProjectId) {
      message.warning('请先上传项目')
      nav('/upload')
      return
    }
    if (selectedModules.length === 0) {
      message.warning('请至少选择一个AI功能模块')
      return
    }
    setLoading(true)
    try {
      const res = await enhanceProject(currentProjectId, selectedModules)
      message.success('AI增强成功，正在下载...')
      window.location.href = `http://localhost:8000${res.data.download_url}`
    } catch {
      message.error('增强失败，请检查项目文件后重试')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ padding: 32, maxWidth: 1000, margin: '0 auto' }}>
      <Typography.Title level={3}>选择AI能力模块</Typography.Title>
      {currentProjectId && (
        <Alert
          message={`当前项目：${currentProjectId.slice(0, 8)}...`}
          type="info"
          style={{ marginBottom: 24 }}
        />
      )}
      <AIModuleSelector />
      <Divider />
      <Button
        type="primary"
        size="large"
        loading={loading}
        onClick={handleEnhance}
        disabled={selectedModules.length === 0}
      >
        开始AI赋能并下载源码包（已选 {selectedModules.length} 个模块）
      </Button>
    </div>
  )
}
