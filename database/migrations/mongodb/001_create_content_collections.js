// GMC Dashboard: MongoDB Content Management Schema
// Document storage for GMC Manual, AI coaching data, and project-scoped content

// Use the GMC Dashboard database
use('gmc_dashboard');

// Create GMC Manual content collection
db.createCollection('gmc_manual_content', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['document_id', 'content_type', 'title', 'content', 'version'],
      properties: {
        document_id: {
          bsonType: 'string',
          description: 'Unique document identifier'
        },
        content_type: {
          bsonType: 'string',
          enum: ['section', 'formula', 'example', 'constraint', 'strategy_guide'],
          description: 'Type of GMC Manual content'
        },
        title: {
          bsonType: 'string',
          description: 'Content title for indexing'
        },
        content: {
          bsonType: 'string',
          description: 'Main content body with markdown support'
        },
        version: {
          bsonType: 'string',
          description: 'Content version for change tracking'
        },
        tags: {
          bsonType: 'array',
          items: { bsonType: 'string' },
          description: 'Content tags for search and categorization'
        },
        educational_level: {
          bsonType: 'string',
          enum: ['beginner', 'intermediate', 'advanced'],
          description: 'Content complexity level'
        },
        related_formulas: {
          bsonType: 'array',
          items: { bsonType: 'string' },
          description: 'Related formula IDs for cross-referencing'
        },
        created_at: {
          bsonType: 'date',
          description: 'Content creation timestamp'
        },
        updated_at: {
          bsonType: 'date',
          description: 'Last content update timestamp'
        }
      }
    }
  }
});

// Create AI coaching sessions collection (project-scoped)
db.createCollection('ai_coaching_sessions', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['coaching_session_id', 'project_id', 'user_id'],
      properties: {
        coaching_session_id: {
          bsonType: 'string',
          description: 'Unique coaching session identifier'
        },
        project_id: {
          bsonType: 'string',
          description: 'Associated project for coaching context isolation'
        },
        user_id: {
          bsonType: 'string',
          description: 'User associated with coaching session'
        },
        conversation_history: {
          bsonType: 'array',
          items: {
            bsonType: 'object',
            required: ['message_id', 'timestamp', 'sender', 'content'],
            properties: {
              message_id: { bsonType: 'string' },
              timestamp: { bsonType: 'date' },
              sender: {
                bsonType: 'string',
                enum: ['user', 'ai']
              },
              content: { bsonType: 'string' },
              project_context_tags: {
                bsonType: 'array',
                items: { bsonType: 'string' }
              },
              ai_provider: {
                bsonType: 'string',
                enum: ['openai', 'anthropic', 'gemini', 'ollama']
              }
            }
          },
          description: 'Project-scoped conversation history'
        },
        strategy_preferences: {
          bsonType: 'object',
          properties: {
            optimization_priorities: {
              bsonType: 'array',
              items: { bsonType: 'string' }
            },
            risk_management_approach: { bsonType: 'string' },
            competitive_focus_areas: {
              bsonType: 'array',
              items: { bsonType: 'string' }
            },
            project_specific_insights: { bsonType: 'object' }
          },
          description: 'Learned user strategy patterns within project'
        },
        decision_patterns: {
          bsonType: 'array',
          items: {
            bsonType: 'object',
            properties: {
              parameter_name: { bsonType: 'string' },
              decision_frequency: { bsonType: 'int' },
              value_ranges: {
                bsonType: 'object',
                properties: {
                  min: { bsonType: 'double' },
                  max: { bsonType: 'double' },
                  preferred: { bsonType: 'double' }
                }
              },
              context_tags: {
                bsonType: 'array',
                items: { bsonType: 'string' }
              }
            }
          },
          description: 'Historical decision-making analysis per project'
        },
        risk_tolerance: {
          bsonType: 'string',
          enum: ['conservative', 'moderate', 'aggressive'],
          description: 'User risk profile for this project'
        },
        learning_progress: {
          bsonType: 'object',
          properties: {
            concepts_mastered: {
              bsonType: 'array',
              items: { bsonType: 'string' }
            },
            areas_for_improvement: {
              bsonType: 'array',
              items: { bsonType: 'string' }
            },
            competency_scores: {
              bsonType: 'object',
              description: 'Subject area competency tracking'
            }
          },
          description: 'Competency development tracking per project'
        },
        coaching_effectiveness: {
          bsonType: 'double',
          minimum: 0.0,
          maximum: 1.0,
          description: 'AI recommendation success rate within project'
        },
        last_interaction: {
          bsonType: 'date',
          description: 'Most recent coaching interaction'
        },
        total_interactions: {
          bsonType: 'int',
          minimum: 0,
          description: 'Conversation volume tracking per project'
        },
        created_at: {
          bsonType: 'date',
          description: 'Session creation timestamp'
        },
        updated_at: {
          bsonType: 'date',
          description: 'Last session update timestamp'
        }
      }
    }
  }
});

// Create project-scoped document storage collection
db.createCollection('project_documents', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['document_id', 'project_id', 'document_type', 'content'],
      properties: {
        document_id: {
          bsonType: 'string',
          description: 'Unique document identifier'
        },
        project_id: {
          bsonType: 'string',
          description: 'Associated project for document isolation'
        },
        document_type: {
          bsonType: 'string',
          enum: ['analysis_notes', 'strategy_memo', 'calculation_worksheet', 'team_notes'],
          description: 'Type of project document'
        },
        title: {
          bsonType: 'string',
          description: 'Document title'
        },
        content: {
          bsonType: 'object',
          description: 'Document content with flexible schema'
        },
        version: {
          bsonType: 'int',
          minimum: 1,
          description: 'Document version number'
        },
        author_user_id: {
          bsonType: 'string',
          description: 'Document creator'
        },
        collaborators: {
          bsonType: 'array',
          items: { bsonType: 'string' },
          description: 'User IDs with document access'
        },
        tags: {
          bsonType: 'array',
          items: { bsonType: 'string' },
          description: 'Document tags for organization'
        },
        is_archived: {
          bsonType: 'bool',
          description: 'Document archive status'
        },
        created_at: {
          bsonType: 'date',
          description: 'Document creation timestamp'
        },
        updated_at: {
          bsonType: 'date',
          description: 'Last document update timestamp'
        }
      }
    }
  }
});

// Create indexes for performance

// GMC Manual Content indexes
db.gmc_manual_content.createIndex({ 'document_id': 1 }, { unique: true });
db.gmc_manual_content.createIndex({ 'content_type': 1, 'educational_level': 1 });
db.gmc_manual_content.createIndex({ 'tags': 1 });
db.gmc_manual_content.createIndex({ 'title': 'text', 'content': 'text' }, { 'name': 'content_search' });

// AI Coaching Sessions indexes  
db.ai_coaching_sessions.createIndex({ 'coaching_session_id': 1 }, { unique: true });
db.ai_coaching_sessions.createIndex({ 'project_id': 1, 'user_id': 1 });
db.ai_coaching_sessions.createIndex({ 'user_id': 1, 'last_interaction': -1 });
db.ai_coaching_sessions.createIndex({ 'project_id': 1, 'coaching_effectiveness': -1 });

// Project Documents indexes
db.project_documents.createIndex({ 'document_id': 1 }, { unique: true });
db.project_documents.createIndex({ 'project_id': 1, 'document_type': 1 });
db.project_documents.createIndex({ 'project_id': 1, 'author_user_id': 1 });
db.project_documents.createIndex({ 'tags': 1 });
db.project_documents.createIndex({ 'title': 'text', 'content': 'text' }, { 'name': 'document_search' });

// Create sample GMC Manual content
db.gmc_manual_content.insertMany([
  {
    document_id: 'capacity_constraints_intro',
    content_type: 'section',
    title: 'Understanding Capacity Constraints',
    content: '# Capacity Constraints in GMC Analysis\n\nCapacity constraints represent the physical limitations of your production facilities. These constraints are fundamental to strategic decision-making as they define the maximum output achievable with available resources.\n\n## Key Concepts:\n- **Machine Hours**: Total available production time\n- **Resource Allocation**: Distributing capacity across product lines\n- **Optimization**: Maximizing output within constraints',
    version: '1.0',
    tags: ['capacity', 'constraints', 'production', 'fundamentals'],
    educational_level: 'beginner',
    related_formulas: ['capacity_formula_basic'],
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    document_id: 'capacity_formula_basic',
    content_type: 'formula',
    title: 'Basic Capacity Constraint Formula',
    content: '## Capacity Constraint Formula\n\n```\nΣ(Machine Hours per Product) ≤ Total Available Machine Hours\n```\n\n### Variables:\n- **Machine Hours per Product**: Hours allocated to each product line\n- **Total Available Machine Hours**: Maximum production capacity\n\n### Educational Note:\nThis formula ensures production decisions remain within physical constraints, preventing unrealistic optimization scenarios.',
    version: '1.0',
    tags: ['formula', 'capacity', 'mathematics'],
    educational_level: 'intermediate',
    related_formulas: [],
    created_at: new Date(),
    updated_at: new Date()
  }
]);

print('MongoDB Content Management collections and indexes created successfully');
print('Sample GMC Manual content inserted');
print('AI coaching sessions and project documents collections ready for use');