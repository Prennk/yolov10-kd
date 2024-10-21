import torch.nn as nn
import torch.nn.functional as F


__all__ = ['CriterionKD']

class CriterionKD(nn.Module):
    '''
    knowledge distillation loss
    '''
    def __init__(self, temperature=5):
        super(CriterionKD, self).__init__()
        self.temperature = temperature

    def forward(self, pred, soft):
        B, N, C = pred.size()
        scale_pred = pred.view(-1, C)
        scale_soft = soft.view(-1, C)
        p_s = F.log_softmax(scale_pred / self.temperature, dim=1)
        p_t = F.softmax(scale_soft / self.temperature, dim=1)
        loss = F.kl_div(p_s, p_t, reduction='batchmean') * (self.temperature**2)
        return loss