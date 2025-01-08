
import authAxios from '@/services/api/setup';
import * as interfaces from './interfaces'

const baseURL = import.meta.env.VITE_API_URL;

/**
 * Uploads lecture session video to make Study Guide
 * @param formData - the from contianing the video data
 */
export const uploadVideoToAIModel = async (lecture_session_id: String, formData: FormData) => {
    try {
        console.log(lecture_session_id)
        const response = await authAxios.post(`${baseURL}/aimodelmanagement/${lecture_session_id}/image_prediction_output`, formData, { headers: { 'Content-Type': 'multipart/form-data' } });
        return response.data;
    } 
    catch(error) {
        console.error("Failed to upload videos", error);
        throw new Error("Failed to upload videos. Please check the provided data and try again.");
    }
}

