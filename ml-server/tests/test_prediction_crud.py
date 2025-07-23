"""Tests for Prediction CRUD operations."""

import pytest
import uuid

from ml_server.domain import (
    PredictionService,
    PredictionNotFoundError,
    InvalidPredictionDataError,
)
from ml_server.infrastructure.repositories.prediction.prediction_repository_inmemory import (
    InMemoryPredictionRepository,
)


class TestPredictionCRUD:
    """Test suite for Prediction CRUD operations."""

    @pytest.fixture
    def repository(self):
        """Create a fresh repository for each test."""
        return InMemoryPredictionRepository()

    @pytest.fixture
    def service(self, repository):
        """Create a service with the repository."""
        return PredictionService(repository)

    @pytest.fixture
    def sample_prediction_data(self):
        """Sample prediction data for testing."""
        return {
            "confidence": 0.95,
            "class": "invoice",
            "metadata": {"processing_time": 0.5},
        }

    @pytest.mark.asyncio
    async def test_create_prediction(self, service, sample_prediction_data):
        """Test creating a new prediction."""
        prediction = await service.create_prediction(
            model_id="test-model",
            prediction_data=sample_prediction_data,
            request_id="test-request",
        )

        assert prediction.model_id == "test-model"
        assert prediction.prediction == sample_prediction_data
        assert prediction.request_id == "test-request"
        assert prediction.prediction_id is not None

    @pytest.mark.asyncio
    async def test_create_prediction_with_custom_id(
        self, service, sample_prediction_data
    ):
        """Test creating a prediction with a custom ID."""
        custom_id = uuid.uuid4()
        prediction = await service.create_prediction(
            model_id="test-model",
            prediction_data=sample_prediction_data,
            request_id="test-request",
            prediction_id=custom_id,
        )

        assert prediction.prediction_id == custom_id

    @pytest.mark.asyncio
    async def test_create_invalid_prediction(self, service):
        """Test creating an invalid prediction."""
        with pytest.raises(InvalidPredictionDataError):
            await service.create_prediction(
                model_id="",  # Empty model_id should be invalid
                prediction_data={},
                request_id="test-request",
            )

    @pytest.mark.asyncio
    async def test_get_prediction_by_id(self, service, sample_prediction_data):
        """Test retrieving a prediction by ID."""
        created_prediction = await service.create_prediction(
            model_id="test-model",
            prediction_data=sample_prediction_data,
            request_id="test-request",
        )

        retrieved_prediction = await service.get_prediction_by_id(
            created_prediction.prediction_id
        )

        assert retrieved_prediction is not None
        assert retrieved_prediction.prediction_id == created_prediction.prediction_id

    @pytest.mark.asyncio
    async def test_get_nonexistent_prediction(self, service):
        """Test retrieving a non-existent prediction."""
        nonexistent_id = uuid.uuid4()
        prediction = await service.get_prediction_by_id(nonexistent_id)

        assert prediction is None

    @pytest.mark.asyncio
    async def test_update_prediction(self, service, sample_prediction_data):
        """Test updating a prediction."""
        created_prediction = await service.create_prediction(
            model_id="test-model",
            prediction_data=sample_prediction_data,
            request_id="test-request",
        )

        new_data = {"confidence": 0.99, "class": "updated"}
        updated_prediction = await service.update_prediction(
            created_prediction.prediction_id, new_prediction_data=new_data
        )

        assert updated_prediction.prediction == new_data

    @pytest.mark.asyncio
    async def test_update_nonexistent_prediction(self, service):
        """Test updating a non-existent prediction."""
        nonexistent_id = uuid.uuid4()

        with pytest.raises(PredictionNotFoundError):
            await service.update_prediction(
                nonexistent_id, new_prediction_data={"confidence": 0.99}
            )

    @pytest.mark.asyncio
    async def test_delete_prediction(self, service, sample_prediction_data):
        """Test deleting a prediction."""
        created_prediction = await service.create_prediction(
            model_id="test-model",
            prediction_data=sample_prediction_data,
            request_id="test-request",
        )

        deleted = await service.delete_prediction(created_prediction.prediction_id)
        assert deleted is True

        # Verify it's deleted
        prediction = await service.get_prediction_by_id(
            created_prediction.prediction_id
        )
        assert prediction is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent_prediction(self, service):
        """Test deleting a non-existent prediction."""
        nonexistent_id = uuid.uuid4()
        deleted = await service.delete_prediction(nonexistent_id)
        assert deleted is False

    @pytest.mark.asyncio
    async def test_get_predictions_by_request_id(self, service, sample_prediction_data):
        """Test retrieving predictions by request ID."""
        request_id = "test-request-123"

        # Create multiple predictions with same request ID
        await service.create_prediction(
            model_id="model-1",
            prediction_data=sample_prediction_data,
            request_id=request_id,
        )
        await service.create_prediction(
            model_id="model-2",
            prediction_data=sample_prediction_data,
            request_id=request_id,
        )

        predictions = await service.get_predictions_by_request_id(request_id)
        assert len(predictions) == 2

    @pytest.mark.asyncio
    async def test_get_predictions_by_model_id(self, service, sample_prediction_data):
        """Test retrieving predictions by model ID."""
        model_id = "test-model-456"

        # Create multiple predictions with same model ID
        await service.create_prediction(
            model_id=model_id,
            prediction_data=sample_prediction_data,
            request_id="req-1",
        )
        await service.create_prediction(
            model_id=model_id,
            prediction_data=sample_prediction_data,
            request_id="req-2",
        )

        predictions = await service.get_predictions_by_model_id(model_id)
        assert len(predictions) == 2

    @pytest.mark.asyncio
    async def test_prediction_exists(self, service, sample_prediction_data):
        """Test checking if a prediction exists."""
        created_prediction = await service.create_prediction(
            model_id="test-model",
            prediction_data=sample_prediction_data,
            request_id="test-request",
        )

        exists = await service.prediction_exists(created_prediction.prediction_id)
        assert exists is True

        nonexistent_id = uuid.uuid4()
        exists = await service.prediction_exists(nonexistent_id)
        assert exists is False

    @pytest.mark.asyncio
    async def test_get_all_predictions_pagination(
        self, service, sample_prediction_data
    ):
        """Test getting all predictions with pagination."""
        # Create multiple predictions
        for i in range(5):
            await service.create_prediction(
                model_id=f"model-{i}",
                prediction_data=sample_prediction_data,
                request_id=f"req-{i}",
            )

        # Test pagination
        page1 = await service.get_all_predictions(limit=2, offset=0)
        assert len(page1) == 2

        page2 = await service.get_all_predictions(limit=2, offset=2)
        assert len(page2) == 2

        page3 = await service.get_all_predictions(limit=2, offset=4)
        assert len(page3) == 1
