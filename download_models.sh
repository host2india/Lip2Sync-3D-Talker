#!/bin/bash
set -e

echo "📥 Downloading all SadTalker models..."

mkdir -p /workspace/models/sadtalker/checkpoints
CKPT=/workspace/models/sadtalker/checkpoints

# ------------ ADD YOUR DRIVE LINKS HERE ------------
declare -A MODELS=(
    ["epoch_20.pth"]="1Yj-s_mOOi0Cze3hMewGfYi1NhvUr9tus"
    ["audo2exp_00300-model.pth"]="1FEeNXMmsgUDGAH2LkIOoXtJSWG9jln1V"
    ["audio2pose_00140-model.pth"]="1-127XXF3jtT39dsQCzA7zrHq_ltbAuP4"
    ["mapping_00109-model.pth.tar"]="1T7Q1gCB-wwlZhym5bX45AWxFOPV-fZYi"
    ["mapping_00229-model.pth.tar"]="1H4cIAn-URt8OEh7ykJW-38AzRpz4bSIM"
    ["epoch_00190.pth.tar"]="1B6-Sark54byn8d9HeAvjqXrcuiY8hxuP"
    ["hubert_soft.pt"]="1Xqhfsr3ZXUlogrwNiFg9Y734cpbrm4zK"
    ["GFV.pth"]="11rhboV2IJZi1q6t34kfvuwxSmWChOuJQ"
    ["facevid2vid_00189-model.pth.tar"]="1BHpU7tErSxtqdNpoA2aqqxR5BnrB46Jx"
    ["shape_predictor_68_face_landmarks.dat"]="18Xiw0JDNe5b0yc0lJ6XJoMb2O7WZ9Pvi"
)

for FILE in "${!MODELS[@]}"; do
    ID="${MODELS[$FILE]}"
    DEST="$CKPT/$FILE"
    if [[ ! -f "$DEST" ]]; then
        echo "⬇️ $FILE"
        gdown "https://drive.google.com/uc?id=$ID" -O "$DEST"
    else
        echo "✔️ Exists: $FILE"
    fi
done

# ----------- BFM_Fitting ------------
echo "📥 Downloading BFM_Fitting..."
mkdir -p $CKPT/BFM_Fitting
gdown --folder --id 1QugS7P7-8x37WfLmRMZf-fykZXaYZLcw -O $CKPT/BFM_Fitting

echo "🎉 All models downloaded!"
